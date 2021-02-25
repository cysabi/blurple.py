import discord

import blurple.ui as ui


class Alert(ui.Base):
    """ A subclass of :class:`discord.Embed` for stylish alert messages.

        :param Style style: The style of the alert.
        :param str title: The title of the alert, will be wrapped in emoji and alert name unless specified in options.
        :param str description: An optional description of the alert, use your imagination for it's use.
        :param **options: Alert options to customize it's look.

            :emoji: Defaults to :class:`True`. Can be set to false to remove the emoji from the alert title.
                This will automatically be removed if a custom style specifies it as an empty string.
            :name: Defaults to :class:`True`. Can be set to false to remove the name of the alert from the title.
                This will automatically be removed if a custom style specifies it as an empty string.
    """

    def __init__(self, style: ui.Style, title: str, description: str = discord.Embed.Empty, **options):
        super().__init__(
            color=style[0],
            title=self.process_title(style, title, **options),
            description=description
        )

    @staticmethod
    def process_title(style: ui.Style, title: str, **options):
        output: str = ''

        if options.get("emoji") is not False and style[1]:
            output += style[1] + " "

        if (name := options.get("name", style[2])) is not False and name:
            output += f"`{name}:` "

        return output + f"**{title}**"
