import discord
from discord.ext import commands, tasks
import requests

# GitHub repository details
github_repo = "mitsuki-jpg/GitBits"
github_api_url = f"https://api.github.com/repos/{github_repo}/releases/latest"

# Discord bot setup
bot = commands.Bot(command_prefix='!')

# Function to get the latest release from GitHub
def get_latest_release():
    response = requests.get(github_api_url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to format release information for Discord embed
def format_embed(release):
    embed = discord.Embed(
        title=release['name'],
        url=release['html_url'],
        description=release['body'],
        color=0x3498db  # You can customize the color here
    )
    embed.set_author(name=release['author']['login'], icon_url=release['author']['avatar_url'])
    embed.set_footer(text="GitHub Release Notification")
    return embed

# Task to check for updates and send messages to Discord channel
@tasks.loop(minutes=30)  # Adjust the interval as needed
async def check_github_updates():
    channel_id = YOUR_DISCORD_CHANNEL_ID  # Replace with your Discord channel ID

    latest_release = get_latest_release()
    if latest_release:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=format_embed(latest_release))

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    check_github_updates.start()

# Run the bot
bot.run('YOUR_BOT_TOKEN')  # Replace with your bot token
