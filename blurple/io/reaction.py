import discord

import blurple.io as io


class ReactionAddBasic(io.Reply):
    """An unopinionated, lower level class to wait for a user to add a reaction."""
    event = "raw_reaction_add"

    async def on_reply_init(self, message: discord.Message):
        """Sepcialized to pass message object."""
        self.message = message

    def reply_check(self, payload: discord.RawReactionActionEvent):
        """Specialized to check if the reaction and payload message is valid."""
        if payload.message_id == self.message.id and not payload.user_id == self.ctx.me.id:
            if self._iscontainer(self.validate):
                return str(payload.emoji) in self.validate
            return True


class ReactionRemoveBasic(ReactionAddBasic):
    """An unopinionated, lower level class to wait for a user to remove a reaction."""
    event = "raw_reaction_remove"


class ReactionAddReply(ReactionAddBasic):
    """ Ask for the user's reaction reply.

        :Example Usage:
        .. code-block:: python

            reply = await io.ReactionAddBasic(ctx, validate=["✅", "❎"]).result()
    """

    async def on_reply_init(self, message: discord.Message):
        """Specialized to add vaild reaction emojis to message, if validation is on."""
        await super().on_reply_init(message)
        if self._iscontainer(self.validate):
            for react in self.validate:
                await self.message.add_reaction(react)

    def reply_check(self, payload: discord.RawReactionActionEvent):
        """Specialized to check if payload user and message are valid."""
        return payload.user_id == self.ctx.author.id and \
               payload.message_id == self.message.id

    async def on_reply_attempt(self, payload: discord.RawReactionActionEvent):
        """Specialized to remove the user's reaction."""
        await self.message.remove_reaction(payload.emoji, self.ctx.bot.get_user(payload.user_id))
        return payload

    async def on_reply_complete(self):
        """Specialized to clear all reactions off the message."""
        await self.message.clear_reactions()
