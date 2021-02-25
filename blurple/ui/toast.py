import asyncio
import discord

import blurple.ui as ui
import blurple.io as io


class ToastInteraction(io.ReactionAddReply):

    async def on_reply_init(self, message):
        await super().on_reply_init(message)
        self.dismiss = "\u2716\ufe0f"
        await self.message.add_reaction(self.dismiss)

    def reply_check(self, payload):
        return super().reply_check(payload) and payload.emoji.name == self.dismiss

    async def on_reply_attempt(self, payload: discord.RawReactionActionEvent):
        return payload

    async def on_reply_complete(self):
        await self.message.delete()


class Toast(ui.Base):
    """ A subclass of :class:`discord.Embed` for stylish toasts.

        The difference between this class and :class:`Alert` is these are intended to hold more deemphasized information.
        These are used with :class:`blurple.io.Toast`, which supports a "dismiss" button to dismiss the toast, and automatic deletion with specified duration.

        :param Style style: The style of the toasts.
        :param str text: The text of the toasts, will be wrapped in an emoji unless specified in options.
        :param **options: Toast options to customize it's look.

            :emoji: Defaults to :class:`True`. Can be set to false to remove the emoji from the toast.
    """

    def __init__(self, style: ui.Style, text: str, **options):
        super().__init__(
            color=style[0],
            description=self.process_text(style, text, **options),
        )

    async def send(self, client, duration=5):
        message = await client.send(embed=self)
        asyncio.create_task(ToastInteraction(client, message=message, timeout=duration).result())

    @classmethod
    def process_text(cls, style: ui.Style, text: str, **options):
        output: str = ''

        if options.get("emoji") is not False:
            output += style[1] + " "

        return output + text
