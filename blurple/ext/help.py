import discord
from discord.ext import commands


class HelpCommand(commands.DefaultHelpCommand):
    """ A drop-in replacement for the default HelpCommand class.

        :param discord.Embed [embed]: Specify a custom :class:`discord.Embed` subclass to use for the help embed, defaults to :class:`discord.Embed`.
        :param dict [embed_args]: Specify custom arguments to pass to the :class:`discord.Embed` class used for the help embed.

        :Example Usage:
        .. code-block:: python

            bot = commands.Bot()
            bot.help_command = ext.HelpCommand()
    """

    def __init__(self, embed: discord.Embed = discord.Embed, embed_args: dict = {}, **options):
        super().__init__(**options)
        self.embed = embed
        self.embed_args = embed_args

    async def send_bot_help(self, mapping):
        """"""
        commands = {k: mapping[k] for k in [None, *list(mapping.keys())[:-1]]}

        embed = self.create_embed(
            title=self.sig('help'),
            description=f"Welcome to the {self.context.bot.user.name} help command!",
            fields=[{
                    "name": self.sig(cog),
                    "value": await self.list_commands(cog_commands)
            } for cog, cog_commands in commands.items() if await self.filter_commands(cog_commands)]
        )
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        """"""
        embed = self.create_embed(
            title=self.sig(cog),
            description=cog.description,
            **({"fields": [{
                "name": "Commands:",
                "value": await self.list_commands(cog.get_commands())
            }]} if cog.get_commands() else {})
        )
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        """"""
        embed = self.create_embed(
            title=self.sig(group, sig=True),
            description=group.help,
            **({"fields": [{
                "name": "Subcommands:",
                "value": await self.list_commands(group.commands)
            }]} if group.commands else {})
        )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        """"""
        embed = self.create_embed(
            title=self.sig(command, sig=True),
            description=command.help,
        )
        await self.get_destination().send(embed=embed)

    async def command_not_found(self, string):
        """"""
        sig = self.sig(string)
        return f"Command {sig} is not found."

    async def subcommand_not_found(self, command, string):
        """"""
        sig = self.sig(command)
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"Command {sig} has no subcommand named `{string}`."
        else:
            return f"Command {sig} has no subcommands."

    async def send_error_message(self, error):
        """"""
        await self.get_destination().send(
            embed=self.create_embed(title="Command Not Found", description=error))

    async def list_commands(self, commands):
        """"""
        return "\n".join([self.sig(command, doc=True) for command in await self.filter_commands(commands)])

    def create_embed(self, fields: list = (), **kwargs):
        """"""
        # Create embed
        embed = self.embed(**{**self.embed_args, **kwargs})
        # Add fields
        for field in fields:
            embed.add_field(**field, inline=False)
        # Set footer
        footer = getattr(embed, '_footer', {})
        footer["text"] = f"Type {self.clean_prefix}help command for more info on a command. You can also type {self.clean_prefix}help category for more info on a category."
        embed.set_footer(**footer)

        return embed

    def sig(self, command, *, doc=False, sig=False):
        """"""
        # Command is cog
        if isinstance(command, commands.Cog):
            return command.qualified_name
        if command is None:
            return '\u200B'
        # Command is regular
        display = self.get_command_signature(command).strip() if sig else f'{self.clean_prefix}{command}'
        return f'`{display}` {(command.short_doc if doc else "")}'
