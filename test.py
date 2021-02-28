import os
import discord
from discord.ext import commands

from blurple import ui, io, ext


bot = commands.Bot(command_prefix='!')
bot.help_command = ext.HelpCommand()
router = ext.Router(bot)

@bot.event
async def on_ready():
    print(f'{bot.user.name}: Ready for Testing')

@router.route(["alert", "styles"])
async def styles(ctx):
    await ui.Alert(ui.Style.PRIMARY, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert(ui.Style.SECONDARY, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert(ui.Style.SUCCESS, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert(ui.Style.DANGER, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert(ui.Style.WARNING, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert(ui.Style.INFO, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert(ui.Style.LIGHT, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert(ui.Style.DARK, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert(ui.Style.GHOST, "This is a test alert", "Check it out!").send(ctx)
    await ui.Alert((0x9266CC, "\U0001f347", "Grape"), "This is a custom style alert", "Check it out!").send(ctx)

@router.route(["alert", "custom"])
async def custom(ctx):
    await ui.Alert(ui.Style.PRIMARY, "Custom Alerts", "Default style").send(ctx)
    await ui.Alert(ui.Style.PRIMARY, "Custom Alerts", "Alternate name", name="Alternate").send(ctx)
    await ui.Alert(ui.Style.PRIMARY, "Custom Alerts", "No name", name=False).send(ctx)
    await ui.Alert(ui.Style.PRIMARY, "Custom Alerts", "No emoji", emoji=False).send(ctx)
    await ui.Alert(ui.Style.PRIMARY, "Custom Alerts", "No emoji, alternate name", emoji=False, name="Alternate").send(ctx)
    await ui.Alert(ui.Style.PRIMARY, "Custom Alerts", "No emoji, no name", emoji=False, name=False).send(ctx)

@router.route(["reply", "message"])
async def message(ctx):
    await ctx.send("Enter a number.")
    reply = await io.MessageReply(ctx, validate=r'^[0-9]{1,}$').result()
    await ui.Alert(ui.Style.SUCCESS, "Valid Reply", reply.content).send(ctx)

@router.route(["reply", "multiple"])
async def multiple(ctx):
    message = await ctx.send("React or send a message")
    reply, result = await io.Reply.result_between({
        io.MessageReply(ctx),
        io.ReactionAddReply(ctx, validate=['☑️','🔘'], message=message)
    })
    await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, reply, io.Reply._get_reply_content(result)))

@router.route(["reply", "reaction"], aliases=["react"])
async def reaction(ctx):
    message = await ctx.send("Enter reaction.")
    reply = await io.ReactionAddReply(ctx,
        validate=["<:primary:808874731763007488>", "<:secondary:808874731758813205>"],
        message=message).result()
    await ui.Toast(ui.Style.SUCCESS, f"Valid Reply: {str(reply.emoji)}").send(ctx)


@router.route(["toast"])
async def toast(ctx):

    message = await ctx.send("Show Toast:")
    await message.add_reaction("<:primary:808874731763007488>")
    while True:
        reply = await io.ReactionAddBasic(ctx,
            validate=["<:primary:808874731763007488>"],
            message=message).result()
        await ui.Toast(ui.Style.SUCCESS, f"Valid Reply: {str(reply.emoji)}").send(ctx)


bot.run(os.getenv("TOKEN"))
