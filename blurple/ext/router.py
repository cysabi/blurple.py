import typing as t
from discord.ext import commands

class Router:
    """ Create a router, connected to a bot instance to allow route-based command registry.

        :Example Usage:
        .. code-block:: python

            bot = commands.Bot()
            router = Router(bot)

            @router.route(["cmd", "subcmd"])
            async def subcmd(ctx):
                pass
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def route(self, command: list, **kwargs):
        """ A shortcut decorator that registers a command route.

            :param list[str] command: A list of strings defining the route to the command.
            :param **kwargs: Any command attributes to pass on, such as aliases.
        """
        def deco(func):
            return self.get_command_group(command, func, **kwargs)
        return deco

    def get_command_group(self, path: list, func: t.Optional[t.Callable] = None, **kwargs) -> commands.Group:
        # Return self.bot if path is the root
        if len(path) == 0:
            return self.bot
        # Try and find group
        group: commands.Group = self.bot.get_command(" ".join(path))
        # If it doesn't exist, create it group
        if group is None or func:
            # Get the parent group
            parent = self.get_command_group(path[:-1])
            existing_subcommands = []
            # Create the func if it doesn't exist
            if func is None:
                async def func(ctx):
                    raise commands.CommandNotFound(f'Command "{path[-1]}" is not found')
            # Remove the current group it already exists
            elif group is not None:
                existing_subcommands = group.commands
                parent.remove_command(group.name)

            # Create the group
            group = commands.Group(func, name=path[-1], invoke_without_command=True, **kwargs)
            # Add existing subcommands
            for cmd in existing_subcommands:
                group.add_command(cmd)
            # Register command
            parent.add_command(group)

        return group
