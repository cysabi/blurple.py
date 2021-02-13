import discord
from discord.ext import commands


class HelpCommand(commands.DefaultHelpCommand):
    """Set up help command for the bot."""

    def __init__(self, color = discord.Embed.Empty, **options):
        super().__init__(**options)
        self.color = color

    async def send_bot_help(self, mapping):
        """Send bot command page."""
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
        """Send cog command page."""
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
        """Send command group page."""
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
        """Send command page."""
        embed = self.create_embed(
            title=self.sig(command, sig=True),
            description=command.help,
        )
        await self.get_destination().send(embed=embed)

    async def command_not_found(self, string):
        """Returns message when command is not found."""
        sig = self.sig(string)
        return f"Command {sig} is not found."

    async def subcommand_not_found(self, command, string):
        """Returns message when subcommand is not found."""
        sig = self.sig(command)
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"Command {sig} has no subcommand named `{string}`."
        else:
            return f"Command {sig} has no subcommands."

    async def send_error_message(self, error):
        """Send error message, override to support sending embeds."""
        await self.get_destination().send(
            embed=self.create_embed(title="Command Not Found", description=error))

    async def list_commands(self, commands):
        """Create a formatted string listing commands in a group."""
        return "\n".join([self.sig(command, doc=True) for command in await self.filter_commands(commands)])

    def create_embed(self, fields: list = (), **kwargs):
        """Create help embed."""
        embed = discord.Embed(color=self.color, **kwargs)
        for field in fields:
            embed.add_field(**field, inline=False)
        embed.set_footer(
            text=f"Type {self.clean_prefix}help command for more info on a command. You can also type {self.clean_prefix}help category for more info on a category.")
        return embed

    def sig(self, command, *, doc=False, sig=False):
        """List the command as a one-liner."""
        # Command is cog
        if isinstance(command, commands.Cog):
            return command.qualified_name
        if command is None:
            return '\u200B'
        # Command is regular
        display = self.get_command_signature(command).strip() if sig else f'{self.clean_prefix}{command}'
        return f'`{display}` {(command.short_doc if doc else "")}'
