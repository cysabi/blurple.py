import discord

import blurple.io as io


class MessageBasic(io.Reply):
    """An unopinionated, lower level class to wait for a user to send a message."""
    event = "message"

    def reply_check(self, reply: discord.Message):
        """Specialized to check if the message is in the same channel by the same author."""
        return reply.author.id == self.ctx.author.id and \
               reply.channel.id == self.ctx.channel.id


class MessageReply(MessageBasic):
    """ Ask for the user's message reply.

        :Example Usage:
        .. code-block:: python

            reply = await io.MessageReply(ctx, validate=["yes", "no"]).result()
    """

    async def on_reply_attempt(self, reply: discord.Message):
        """Specialized to delete the reply on attempt."""
        await reply.delete()
