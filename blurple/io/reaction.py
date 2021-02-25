import discord

import blurple.io as io


class ReactionAddReply(io.Reply):
    event = "raw_reaction_add"

    async def on_reply_init(self, message):
        """Specialized to add vaild reaction emojis to message, if validation is on."""
        self.message = message
        if self._iscontainer(self.validate):
            for react in self.validate:
                await self.message.add_reaction(react)

    def reply_check(self, payload):
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
