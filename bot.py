import os
import re
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

discord_bot = os.environ.get('DISCORD_BOT') 

# Initialize the bot
intents = discord.Intents.default()
# Note: We don't even need message_content intent anymore for slash commands!
bot = commands.Bot(command_prefix="!", intents=intents)

# RegEx patterns to clean up links
INSTAGRAM_PATTERN = re.compile(r'(https?://(?:www\.)?instagram\.com/(?:p|reel|tv)/[a-zA-Z0-9_\-]+/?)(?:\?\S*)?')
YOUTUBE_PATTERN = re.compile(r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[a-zA-Z0-9_\-]+)')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        # This syncs the slash commands globally with Discord's servers
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Defining the slash command /embeed
@bot.tree.command(name="embeed", description="Easily render and embed Instagram or YouTube videos.")
@app_commands.describe(link="The Instagram post/reel or YouTube link you want to embed")
async def embeed(interaction: discord.Interaction, link: str):
    url = link.strip()
    
    # 1. Handle Instagram
    if "instagram.com" in url:
        fixed_url = url.replace("instagram.com", "oginstagram.com")
        clean_match = INSTAGRAM_PATTERN.search(fixed_url)
        if clean_match:
            fixed_url = clean_match.group(1)
            
        await interaction.response.send_message(fixed_url)
        
    # 2. Handle YouTube
    elif "youtube.com" in url or "youtu.be" in url:
        clean_match = YOUTUBE_PATTERN.search(url)
        final_url = clean_match.group(1) if clean_match else url
        await interaction.response.send_message(final_url)
        
    # 3. Fallback for other links
    else:
        # ephemeral=True means only YOU see this error message, keeping the channel clean
        await interaction.response.send_message(
            "❌ Unsupported link type. Please use a valid Instagram or YouTube link.", 
            ephemeral=True
        )

# Replace with your actual Discord Bot Token
bot.run(discord_bot)
