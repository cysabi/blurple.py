import re
import inspect
import typing as t
from abc import ABC
import discord
from discord.ext import commands
import asyncio

from blurple.ui import Alert


class Reply(ABC):
    """ Get a reply from the user.

        :param ctx: The discord.ext.commands.Context variable
        :param validate: An optional parameter to validate the reply.
            If left blank, no validation will be performed.
            If you pass a list/set, validation will succeed when the reply content is found inside the list/set.
            If you pass a string, validation will succeed when the reply content matches the string as a regex.
            If you pass a function or coroutine, the function will be called, and the coroutine awaited.
                Validation will succeed when the function returns a Truthy value.
                The reply object will be passed as a parameter.
        :param error: An optional parameter specifying the message to send when the user fails validation, defaults to a simple "Invalid Reply" alert.
        :return: A :Reply: object.
    """

    def __init__(self,
            ctx: commands.Context,
            *,
            validate: t.Optional[t.Union[str, t.Callable, t.List]] = None,
            on_error: t.Union[str, discord.Embed] = Alert(Alert.Style.DANGER, "Invalid Reply"),
            timeout = 180,
            **kwargs) -> None:
        """Set up the reply class instance

        .isTimeout
        .message
        .author
        .how_long_it_took_to_reply
        """
        # Set up
        self.ctx = ctx
        self.validate = validate
        self.on_error = on_error
        self.error = None
        self.timeout = timeout
        self.kwargs = kwargs

    async def result(self):
        """Await the result of the reply."""
        await self.on_reply_init(**self.kwargs)  # Event method
        reply = await self.get_valid_reply()
        await self.on_reply_complete()  # Event method
        return reply

    async def get_valid_reply(self):
        """Wrap get_reply with validation, error handling, and recursive calls."""
        reply = await self.get_reply()

        if reply is not None:  # Reply hasn't timed out
            # Validate reply
            is_valid = await self.validate_reply(reply, self.validate)
            # If reply isn't valid, recursively call function
            if not is_valid:
                await self.send_error()
                return await self.get_valid_reply()

        await self.delete_error()
        return reply

    async def get_reply(self):
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

    async def send_error(self) -> discord.Message:
        """ Send an error message to the user.

            Will replace the current error message.
            :param error: An embed or a string representing the error message.
        """
        await self.delete_error()
        if isinstance(self.on_error, discord.Embed):
            self.error = await self.ctx.send(embed=self.on_error)
        elif isinstance(self.on_error, str):
            self.error = await self.ctx.send(self.on_error)
        return self.error

    async def delete_error(self) -> None:
        """Delete the current error message, if it exists."""
        if self.error is None:
            return
        await self.error.delete()
        self.error = None

    @classmethod
    async def validate_reply(cls, reply, valid) -> bool:
        if valid is None:
            return True
        content = cls.get_reply_content(reply)
        if isinstance(valid, str):
            return bool(re.search(valid, content))
        if cls.is_container(valid):
            return content in valid
        if callable(valid):
            if inspect.iscoroutinefunction(object):
                return await valid()
            return valid()

    @staticmethod
    def get_reply_content(reply):
        """Retrieve the content of the reply."""
        if isinstance(reply, discord.Message):
            return reply.content
        if isinstance(reply, discord.Reaction):
            return str(reply.emoji)

    @staticmethod
    def is_container(obj: t.Collection):
        return getattr(obj, "__contains__", False)

    async def on_reply_init(self):
        """Runs on reply class creation."""

    async def on_pre_reply(self):
        """Runs before wait_for event."""

    def reply_check(self, reply):
        """The check to authorize reply."""

    async def on_reply_attempt(self, reply):
        """ Any actions to do after each reply attempt, can be run multiple times if validation is on.

            :return: You can optionally return a parsed version of the reply to be used instead of the raw reply object.
        """

    async def on_reply_complete(self):
        """Any actions to do after reply is completely done, only runs once reply is validated and returned."""


class MessageReply(Reply):
    event = "message"

    def reply_check(self, reply: discord.Message):
        return reply.author.id == self.ctx.author.id and \
               reply.channel.id == self.ctx.channel.id and \
               not reply.content.startswith("\\")

    async def on_reply_attempt(self, reply: discord.Message):
        await reply.delete()


class ReactionAddReply(Reply):
    event = "reaction_add"

    async def on_reply_init(self, message):
        self.message = message
        if self.is_container(self.validate):
            for react in self.validate:
                await self.message.add_reaction(react)

    def reply_check(self, reply, user):
        return user.id == self.ctx.author.id and \
               reply.message.id == self.message.id

    async def on_reply_attempt(self, reply: t.Tuple[discord.Reaction, discord.Member]):
        await self.message.remove_reaction(reply[0].emoji, self.ctx.author)
        return reply[0]

    async def on_reply_complete(self):
        await self.message.clear_reactions()
