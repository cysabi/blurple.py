from abc import ABC
import discord


class Base(discord.Embed, ABC):

    async def send(self, client):
        """ Send the component as a message in discord.

        :param client: The client used, can be :class:`discord.Message`, :class:`commands.Context` or any other :class:`discord.Messageable`.
        :returns: :class:`discord.Message`
        """
        return await client.send(embed=self)
