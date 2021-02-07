import os
import discord
from discord.ext import commands

from blurple import ui

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot}: Ready for Testing')

@bot.command()
async def ping(ctx):
    await ctx.send(embed=ui.Alert("success",
        title="Pong!",
        description=f"Latency: `{round(bot.latency*1000)}ms`")
    )

@bot.command()
async def alert(ctx, sub="styles"):
    if sub == "styles":
        await ctx.send(embed=ui.Alert("primary", "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert("secondary", "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert("success", "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert("danger", "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert("warning", "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert("info", "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert("light", "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert("dark", "This is a test alert", "Check it out!"))
    if sub == "custom":
        await ctx.send(embed=ui.Alert("primary", "Custom Alerts", "Default style"))
        await ctx.send(embed=ui.Alert("primary", "Custom Alerts", "Alternate name", name="Alternate"))
        await ctx.send(embed=ui.Alert("primary", "Custom Alerts", "No name", name=False))
        await ctx.send(embed=ui.Alert("primary", "Custom Alerts", "No emoji", emoji=False))
        await ctx.send(embed=ui.Alert("primary", "Custom Alerts", "No emoji, alternate name", emoji=False, name="Alternate"))
        await ctx.send(embed=ui.Alert("primary", "Custom Alerts", "No emoji, no name", emoji=False, name=False))


bot.run(os.getenv("TOKEN"))
