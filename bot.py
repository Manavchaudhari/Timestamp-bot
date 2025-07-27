import discord
from discord.ext import commands
import os
import parsedatetime  # Natural language date parsing
from datetime import datetime
from tzlocal import get_localzone  # For system's local timezone

# Load token directly from environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
print("DEBUG: DISCORD_TOKEN exists?", bool(TOKEN))
if not TOKEN:
    raise ValueError("ERROR: DISCORD_TOKEN is missing!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# HYBRID COMMAND
@bot.hybrid_command(name="timestamp", description="Convert a natural language date/time to a Discord timestamp")
async def timestamp(ctx: commands.Context, *, datetime_str: str):
    """
    Convert natural language date/time into a Discord timestamp.
    Examples:
      !timestamp tomorrow 8pm
      !timestamp july 28 2025 6pm
    """
    try:
        # Use parsedatetime for better natural language support
        cal = parsedatetime.Calendar()
        naive_dt, parse_status = cal.parseDT(datetime_str, datetime.now())

        if parse_status == 0:  # Failed to parse
            raise ValueError("Could not parse date/time.")

        # Apply system's local timezone (ZoneInfo compatible)
        local_tz = get_localzone()
        dt = naive_dt.replace(tzinfo=None).astimezone(local_tz)

        print(f"[DEBUG] Parsed datetime: {dt} (Local TZ: {local_tz})")
        print(f"[DEBUG] UNIX timestamp: {int(dt.timestamp())}")

        unix_time = int(dt.timestamp())
        await ctx.send(f"Here’s your timestamp: <t:{unix_time}:f>")
    except Exception as e:
        print(f"[ERROR] {e}")
        await ctx.send(
            "Invalid date/time! Examples: `!timestamp july 28 2025 6pm` or `!timestamp tomorrow 8pm`."
        )

bot.run(TOKEN)
