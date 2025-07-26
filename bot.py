import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import dateparser  # Natural language date parsing

# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="timestamp", description="Convert a natural language date/time to a Discord timestamp")
async def timestamp(interaction: discord.Interaction, *, datetime_str: str):
    """
    Convert natural language date/time into a Discord timestamp.
    Examples:
      /timestamp july 28 2025 6pm
      /timestamp tomorrow 8pm
      /timestamp 28th july 2025 18:00
    """
    try:
        dt = dateparser.parse(datetime_str)
        if not dt:
            raise ValueError("Could not parse date/time.")

        unix_time = int(dt.timestamp())
        await interaction.response.send_message(
            f"Here’s your timestamp: <t:{unix_time}:f>"
        )
    except Exception:
        await interaction.response.send_message(
            "Invalid date/time! Try examples like: `/timestamp july 28 2025 6pm` or `/timestamp tomorrow 8pm`."
        )

bot.run(TOKEN)
