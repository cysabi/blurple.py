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
        """
        def deco(func):
            return self.get_command_group(command, func, **kwargs)
        return deco

    def get_command_group(self, path: list, func = None, **kwargs):
        """ Get command group.

            :meta private:
        """
        if len(path) == 0:
            return self.bot
        # Try and find group
        group = self.bot.get_command(" ".join(path))
        # If it doesn't exist, create it group
        if group is None:
            # Get the parent group
            parent = self.get_command_group(path[:-1])
            # Create the func if it doesn't exist
            if func is None:
                async def func(ctx):
                    raise commands.CommandNotFound(f'Command "{path[-1]}" is not found')
            # Create the group
            group = commands.Group(func, name=path[-1], invoke_without_command=True, **kwargs)
            parent.add_command(group)
        # If it does exist, but needs to be overwritten, update callback
        elif func:
            group.callback = func

        return group