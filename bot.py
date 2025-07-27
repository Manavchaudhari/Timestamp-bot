import discord
from discord.ext import commands
import os
import parsedatetime
from datetime import datetime
import pytz
from tzlocal import get_localzone

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

@bot.hybrid_command(name="timestamp", description="Convert a natural language date/time to a Discord timestamp")
async def timestamp(ctx: commands.Context, *, datetime_str: str):
    try:
        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parseDT(datetime_str, datetime.now())

        if parse_status == 0:  # Failed to parse
            raise ValueError("Could not parse date/time.")

        # Apply system's local timezone
        local_tz = get_localzone()
        dt = local_tz.localize(time_struct.replace(tzinfo=None))

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
