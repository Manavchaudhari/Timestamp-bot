import discord
from discord.ext import commands
import os
import dateparser  # Natural language date parsing

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
        # Parse date/time using local timezone
        dt = dateparser.parse(
            datetime_str,
            settings={
                'TIMEZONE': 'local',
                'TO_TIMEZONE': 'local',
                'RETURN_AS_TIMEZONE_AWARE': True
            }
        )

        if not dt:
            raise ValueError("Could not parse date/time.")

        unix_time = int(dt.timestamp())
        await ctx.send(f"Here’s your timestamp: <t:{unix_time}:f>")
    except Exception:
        await ctx.send(
            "Invalid date/time! Examples: `!timestamp july 28 2025 6pm` or `!timestamp tomorrow 8pm`."
        )

bot.run(TOKEN)
