import os
import discord
from dotenv import load_dotenv
from discord_event_monitor import register_events

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

register_events(client)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(TOKEN)