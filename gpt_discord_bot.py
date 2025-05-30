import discord
import openai
import asyncio
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN =  os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🤖 Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ask "):
        user_message = message.content[5:]

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("Something went wrong. Error: " + str(e))

client.run(DISCORD_TOKEN)
