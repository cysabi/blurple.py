import os
import discord

import ui

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client}: Ready for Testing')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Test alerts
    if message.content.startswith('?alert'):
        await message.channel.send(embed=ui.Alert("primary", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("secondary", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("success", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("danger", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("warning", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("info", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("light", "This is a test alert", "Check it out!"))
        await message.channel.send(embed=ui.Alert("dark", "This is a test alert", "Check it out!"))

client.run(os.getenv("TOKEN"))
