from __future__ import annotations
import re
import inspect
import typing as t
from abc import ABC
import discord
from discord.ext import commands
import asyncio

import blurple.ui as ui


class Reply(ABC):
    """ An abstract class for getting replies, to be extended.

        If you are trying to get a reply from the user directly, you may be looking for :class:`MessageReply` or :class:`ReactionAddReply`.

        :Extending this class::
        In order to extend this class, there are 5 methods you can specialize.

        - :func:`on_reply_init` Use this method to initialize variables at the start.
        - :func:`on_pre_reply` Use this method to prepare anything before reply attempts.
        - :func:`reply_check` This is required. Evaluate whether an event call is considered a user reply attempt.
        - :func:`on_reply_attempt` Use this method to handle resetting the state after a reply attempt.
        - :func:`on_reply_complete` Use this method to handle final cleanup.

        :param ctx: The :class:`~commands.Context` variable
        :param validate: An optional parameter to validate the reply.

            - If left blank, no validation will be performed.
            - If you pass a :class:`list` / :class:`set`, validation will succeed when the reply content is found inside the list/set.
            - If you pass a :class:`str`, validation will succeed when the reply content matches the string as a regex.
            - If you pass a :class:`function` or :class:`coroutine`, the function will be called, and the coroutine awaited, validation will succeed when the function returns a Truthy value. The reply object will be passed as a parameter.

        :param on_error: An optional parameter specifying the message to send when the user fails validation, defaults to a simple "Invalid Reply" :class:`~Alert`.
        :param timeout: An optional parameter to change the default timeout length, defaults to 180 seconds.
        :param **kwargs: Any additional parameters that will be passed to :func:`on_reply_init`. This can be useful if you are extending this class and need to take extra parameters when initializing.
    """

    def __init__(self,
            ctx: commands.Context,
            *,
            validate: t.Optional[t.Union[str, t.Callable, t.List]] = None,
            on_error: t.Union[str, discord.Embed] = ui.Alert(ui.Style.DANGER, title="Invalid Reply"),
            timeout = 180,
            **kwargs) -> None:
        self.ctx = ctx
        self.validate = validate
        self.on_error = on_error
        self.error = None
        self.timeout = timeout
        self.kwargs = kwargs

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"<{self.__class__.__name__} for '{self.event}'>"

    async def result(self):
        """Await the result of the reply."""
        await self.on_reply_init(**self.kwargs)  # Event method
        reply = await self._get_valid_reply()
        await self._cleanup()  # Event method
        return reply

    async def _cleanup(self):
        """Clean up reply after result."""
        await self.on_reply_complete()
        await self._delete_error()

    async def _get_valid_reply(self):
        """Wrap get_reply with validation, error handling, and recursive calls."""
        reply = await self._get_reply()

        if reply is not None:  # Reply hasn't timed out
            # Validate reply
            is_valid = await self._validate_reply(reply, self.validate)
            # If reply isn't valid, recursively call function
            if not is_valid:
                await self._send_error()
                return await self._get_valid_reply()

        return reply

    async def _get_reply(self):
        """Get a reply from the user, no validation."""
        await self.on_pre_reply()  # Event method
        # Wait for reply
        try:
            raw_reply = await self.ctx.bot.wait_for(
                self.event,
                check=self.reply_check,
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            reply = None
        else:
            r = await self.on_reply_attempt(raw_reply)  # Event method
            reply = r if r else raw_reply
        return reply

    async def _send_error(self) -> discord.Message:
        """ Send an error message to the user.

            Will replace the current error message.
            :param error: An embed or a string representing the error message.
        """
        await self._delete_error()
        if isinstance(self.on_error, discord.Embed):
            self.error = await self.ctx.send(embed=self.on_error)
        elif isinstance(self.on_error, str):
            self.error = await self.ctx.send(self.on_error)
        return self.error

    async def _delete_error(self) -> None:
        """Delete the current error message, if it exists."""
        if self.error is None:
            return
        await self.error.delete()
        self.error = None


    @classmethod
    async def _validate_reply(cls, reply, valid: t.Union[str, t.Container, t.Callable]) -> bool:
        """Detect validation type and check it against the reply."""
        if valid is None:
            return True
        content = cls._get_reply_content(reply)
        if isinstance(valid, str):
            return bool(re.search(valid, content))
        if cls._iscontainer(valid):
            return content in valid
        if callable(valid):
            if inspect.iscoroutinefunction(object):
                return await valid()
            return valid()

    @staticmethod
    def _get_reply_content(reply):
        """ Retrieve the content of the reply."""
        if isinstance(reply, discord.Message):
            return reply.content
        if isinstance(reply, (discord.Reaction, discord.RawReactionActionEvent)):
            return str(reply.emoji)

    @staticmethod
    def _iscontainer(obj: t.Union[t.Container, t.Any]):
        return getattr(obj, "__contains__", False)

    @classmethod
    async def result_between(cls, replies: t.Container[Reply]) -> t.Tuple[Reply, t.Any]:
        """ Return the first completed result between multiple reply objects.

            :param replies: A collection of Reply objects.
            :returns: A tuple containing the Reply object and the result it returned.

            :How to use this:
            This can be an especially powerful function if used correctly.
            Here's an example of an rsvp list interaction with reactions using this function.

            This is completely contrived for example and not a practical use.

            .. code-block:: python

                rsvp_react = "..."  # Replace this with whatever you want
                rsvp_list = []

                # Start the reply wait
                message = await ctx.send("React to RSVP!")
                await message.add_reaction(rsvp_react)

                add = io.ReactionAddBasic(message, validate=[rsvp_react])
                remove = io.ReactionRemoveBasic(message, validate=[rsvp_react])

                while True:
                    obj, result = io.Reply.result_between({add, remove})
                    if obj is add:
                        rsvp_list.append(result.user_id)
                    elif obj is remove:
                        rsvp_list.remove(result.user_id)
                    else:  # obj is None (The reply timed out)
                        break

                # Reply wait complete
                await message.clear_reactions()
                await message.edit(f"Here's the list of RSVPrs:\\n{'\\n'.join([f'> <@{user_id}>' for user_id in rsvp_list])}")
        """
        # Prepare tasks
        timeouts = []

        def parse_task(reply: Reply):
            # Handle timeout
            timeouts.append(reply.timeout)
            reply.timeout = None
            # Return task
            return asyncio.create_task(reply.result(), name=reply)

        # Wait tasks
        tasks = [parse_task(task) for task in replies]
        task, result = await cls._wait_tasks(tasks, timeout=min(timeouts))

        # Get original reply object
        for obj in replies:
            if task is None:
                obj = None
                break
            if str(obj) == task.get_name():
                break
        # Run cleanup on cancelled replies
        replies.remove(obj)
        for cancelled in replies:
            await cancelled._cleanup()

        # Return original reply object and the result
        return obj, result

    @staticmethod
    async def _wait_tasks(tasks: t.Container[asyncio.Task], timeout: int) -> t.Tuple[t.Optional[asyncio.Future], t.Optional[t.Any]]:
        """ Try block to asyncio.wait a set of tasks with timeout handling.

            :param tasks: A collection of task objects
            :param timeout: How long in seconds to wait until a timeout occurs.
            :return: A tuple containing the task and the result. Both will be None if a timeout occurs.
        """
        done, pending = await asyncio.wait(tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
        for rest in pending:
            rest.cancel()

        if done:
            task: asyncio.Future = done.pop()
            return task, task.result()

        return None, None

    async def on_reply_init(self):
        """ An abstract method, to be extended in custom Reply listeners.

            This method runs when the Reply class is created.
        """

    async def on_pre_reply(self):
        """ An abstract method, to be extended in custom Reply listeners.

            This method runs before each reply attempt, can run multiple times with validation.
        """

    def reply_check(self, reply):
        """ An abstract method, to be extended in custom Reply listeners.

            This method runs as a check to determine whether to recognize the reply event, can run multiple times with validation.
        """

    async def on_reply_attempt(self, reply):
        """ An abstract method, to be extended in custom Reply listeners.

            This method runs after each reply attempt, can run multiple times with validation.

            :return: You can optionally return a parsed version of the reply to be used instead of the raw reply object.
        """

    async def on_reply_complete(self):
        """ An abstract method, to be extended in custom Reply listeners.

            This method runs after a valid reply is returned.
        """
