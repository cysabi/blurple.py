import os
from discord.ext import commands

from blurple import ui, io

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name}: Ready for Testing')

@bot.command()
async def reply(ctx, sub="message"):
    if sub == "message":
        await ctx.send("Enter a number.")
        reply = await io.MessageReply(ctx, validate=r'^[0-9]{1,}$').result()
        await ctx.send(embed=ui.Alert(ui.Alert.Style.SUCCESS, "Valid Reply", reply.content))
    if sub == "reaction":
        message = await ctx.send("Enter reaction.")
        reply = await io.ReactionAddReply(ctx,
            validate=["<:primary:808874731763007488>", "<:secondary:808874731758813205>"],
            message=message).result()
        await ctx.send(embed=ui.Alert(ui.Alert.Style.SUCCESS, "Valid Reply", str(reply.emoji)))


@bot.command()
async def ping(ctx):
    await ctx.send(embed=ui.Alert(ui.Alert.Style.SUCCESS,
        title="Pong!",
        description=f"Latency: `{round(bot.latency*1000)}ms`")
    )

@bot.command()
async def alert(ctx, sub="styles"):
    if sub == "styles":
        await ctx.send(embed=ui.Alert(ui.Alert.Style.PRIMARY, "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.SECONDARY, "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.SUCCESS, "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.DANGER, "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.WARNING, "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.INFO, "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.LIGHT, "This is a test alert", "Check it out!"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.DARK, "This is a test alert", "Check it out!"))
    if sub == "custom":
        await ctx.send(embed=ui.Alert(ui.Alert.Style.PRIMARY, "Custom Alerts", "Default style"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.PRIMARY, "Custom Alerts", "Alternate name", name="Alternate"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.PRIMARY, "Custom Alerts", "No name", name=False))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.PRIMARY, "Custom Alerts", "No emoji", emoji=False))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.PRIMARY, "Custom Alerts", "No emoji, alternate name", emoji=False, name="Alternate"))
        await ctx.send(embed=ui.Alert(ui.Alert.Style.PRIMARY, "Custom Alerts", "No emoji, no name", emoji=False, name=False))


bot.run(os.getenv("TOKEN"))
