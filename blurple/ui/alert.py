import discord


class Alert(discord.Embed):

    styles = {
        "primary": (0x7289DA, "<:primary:807729299603980308>"),
        "secondary": (0x99AAB5, "<:secondary:807729299531759637>"),
        "success": (0x77B255, "\u2705"),
        "danger": (0xDD2E44, "\U0001f6ab"),
        "warning": (0xFFCC4D, "\u26a0\ufe0f"),
        "info": (0x3B88C3, "\u2139\ufe0f"),
        "light": (0xE6E7E8, "\U0001f533"),
        "dark": (0x31373D, "\U0001f532"),
    }

    def __init__(self, style, title: str, description: str = discord.Embed.Empty):
        super().__init__(
            color=self.styles[style][0],
            title=self.process_title(style, title),
            description=description
        )

    @classmethod
    def process_title(cls, style, title):
        return f"{cls.styles[style][1]} `{style.capitalize()}:` **{title}**"
