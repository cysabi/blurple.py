from enum import Enum
import discord


class Alert(discord.Embed):

    class Style(Enum):
        PRIMARY = (0x7289DA, "<:primary:808860644865998848>")
        SECONDARY = (0x99AAB5, "<:secondary:808860792555962389>")
        SUCCESS = (0x77B255, "\u2705")
        DANGER = (0xDD2E44, "\U0001f6ab")
        WARNING = (0xFFCC4D, "\u26a0\ufe0f")
        INFO = (0x3B88C3, "\u2139\ufe0f")
        LIGHT = (0xE6E7E8, "\U0001f533")
        DARK = (0x31373D, "\U0001f532")

        def __getitem__(self, key):
            return self.value[key]

    def __init__(self, style: Style, title: str, description: str = discord.Embed.Empty, **kwargs):
        super().__init__(
            color=style[0],
            title=self.process_title(style, title, **kwargs),
            description=description
        )

    @classmethod
    def process_title(cls, style: Style, title: str, **kwargs):
        output: str = ''

        if kwargs.get("emoji") is not False:
            output += style[1] + " "

        if (name := kwargs.get("name", style.name.capitalize())) is not False:
            output += f"`{name}:` "

        return output + f"**{title}**"
