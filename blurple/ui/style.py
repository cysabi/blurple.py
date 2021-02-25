from enum import Enum


class Style(Enum):
    """ A contextual class to style components.

    There are 9 `main styles <https://cdn.discordapp.com/attachments/598870131182927873/814573079371448330/unknown.png>`_.

    - ``PRIMARY``
    - ``SECONDARY``
    - ``SUCCESS``
    - ``DANGER``
    - ``WARNING``
    - ``INFO``
    - ``LIGHT``
    - ``DARK``
    - ``GHOST``

    You can also create a `custom style <https://cdn.discordapp.com/attachments/598870131182927873/811087938678685707/unknown.png>`_:

    :Example Usage:
    .. code-block:: python

        grape_style = (0x9266CC, "\\U0001f347", "Grape")

    ``PRIMARY`` and ``SECONDARY`` styles use custom emoji, so are unable to be used out of the box.
    To work around this, I've provided the source .svgs in the repository for the custom emojis used throughout the project. you can add these to a server that your bot is in, then create a custom style.

    Alternatively, if you want, you can support me on `ko-fi <https://ko-fi.com/s/7705c20532>`_, and I'll invite your bot to my server with the original custom emojis.

    """
    PRIMARY = (0x7289DA, "<:primary:808874731763007488>", "Primary")
    SECONDARY = (0x99AAB5, "<:secondary:808874731758813205>", "Secondary")
    SUCCESS = (0x77B255, "\u2705", "Success")
    DANGER = (0xDD2E44, "\U0001f6ab", "Danger")
    WARNING = (0xFFCC4D, "\u26a0\ufe0f", "Warning")
    INFO = (0x3B88C3, "\u2139\ufe0f", "Info")
    LIGHT = (0xE6E7E8, "\U0001f533", "Light")
    DARK = (0x31373D, "\U0001f532", "Dark")
    GHOST = (0x2f3136, "", "")

    def __getitem__(self, key):
        return self.value[key]
