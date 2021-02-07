import os
import discord

from blurple import ui

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client}: Ready for Testing')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Test alerts
    if message.content == '.alert style':
        await message.channel.send(embed=ui.Alert("primary", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("secondary", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("success", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("danger", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("warning", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("info", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("light", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("dark", "This is a test alert", "Check it out!"))
    if message.content == '.alert custom':
        await message.channel.send(embed=ui.Alert("primary", "Custom Alerts", "Default style"))
        await message.channel.send(embed=ui.Alert("primary", "Custom Alerts", "Alternate name", name="Alternate"))
        await message.channel.send(embed=ui.Alert("primary", "Custom Alerts", "No name", name=False))
        await message.channel.send(embed=ui.Alert("primary", "Custom Alerts", "No emoji", emoji=False))
        await message.channel.send(embed=ui.Alert("primary", "Custom Alerts", "No emoji, alternate name", emoji=False, name="Alternate"))
        await message.channel.send(embed=ui.Alert("primary", "Custom Alerts", "No emoji, no name", emoji=False, name=False))


client.run(os.getenv("TOKEN"))
