from abc import ABC
import discord


class Base(discord.Embed, ABC):

    async def send(self, client: discord.abc.Messageable):
        """ Send the component as a message in discord.

        :param client: The client used, usually a :class:`discord.abc.Messageable`. Must have implemented :func:`.send`
        :returns: :class:`discord.Message`
        """
        return await client.send(embed=self)
