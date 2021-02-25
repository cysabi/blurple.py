import asyncio
import discord

import blurple.ui as ui
import blurple.io as io

class Toast(discord.Embed):
    """ A subclass of :class:`discord.Embed` for stylish toasts.

        The difference between this class and :class:`Alert` is these are intended to hold more deemphasized information.
        These are used with :class:`blurple.io.Toast`, which supports a "dismiss" button to dismiss the toast, and automatic deletion with specified duration.

        :param Style style: The style of the toasts.
        :param str text: The text of the toasts, will be wrapped in an emoji unless specified in options.
        :param **options: Toast options to customize it's look.

            :emoji: Defaults to :class:`True`. Can be set to false to remove the emoji from the toast.
    """

    def __init__(self, style: Style, text: str, **options):
        super().__init__(
            color=style[0],
            description=self.process_text(style, text, **options),
        )

    @classmethod
    def process_text(cls, style: Style, text: str, **options):
        output: str = ''

        if options.get("emoji") is not False:
            output += style[1] + " "

        return output + text
