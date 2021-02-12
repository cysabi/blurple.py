from enum import Enum
import discord


class Alert(discord.Embed):
    """ A subclass of discord.Embed for stylish alert messages.

        :param style: A contextual class describing the style of the alert.
            There are 8 main alert styles, but you can also provide your own style in the form of a (color, emoji) tuple.
            Primary and Secondary styles use custom emoji, so are unable to be used out of the box.
            To work around this, I've provided the source .svgs in the repository for the custom emojis used throughout the project. you can add these to a server that your bot is in, then create a custom style.
            Alternatively, if you want, you can support me on [ko-fi](https://ko-fi.com/s/7705c20532), and I'll invite your bot to my server where it'll have access to the original custom emojis.
        :param title: The title of the alert, will be wrapped in emoji and alert name unless specified in options.
        :param description: An optional description of the alert, use your imagination for it's use.
        :param **options: Alert options to customize it's look.
            - `emoji`: Defaults to `True`. Can be set to false to remove the emoji from the alert title.
            - `name`: Defaults to `True`. Can be set to false to remove the name of the alert from the title.
    """

    class Style(Enum):
        PRIMARY = (0x7289DA, "<:primary:808874731763007488>")
        SECONDARY = (0x99AAB5, "<:secondary:808874731758813205>")
        SUCCESS = (0x77B255, "\u2705")
        DANGER = (0xDD2E44, "\U0001f6ab")
        WARNING = (0xFFCC4D, "\u26a0\ufe0f")
        INFO = (0x3B88C3, "\u2139\ufe0f")
        LIGHT = (0xE6E7E8, "\U0001f533")
        DARK = (0x31373D, "\U0001f532")

        def __getitem__(self, key):
            return self.value[key]

    def __init__(self, style: Style, title: str, description: str = discord.Embed.Empty, **options):
        super().__init__(
            color=style[0],
            title=self.process_title(style, title, **options),
            description=description
        )

    @classmethod
    def process_title(cls, style: Style, title: str, **options):
        output: str = ''

        if options.get("emoji") is not False:
            output += style[1] + " "

        if (name := options.get("name", style.name.capitalize())) is not False:
            output += f"`{name}:` "

        return output + f"**{title}**"
