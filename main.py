from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, TextChannel, app_commands
from discord.ext import commands
import settings

import msg_logging
import generation

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TKN')
PREFIX: Final[str] = os.getenv('PREXIX')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    await bot.tree.sync()
    

@bot.event
async def on_message(message):
    
    # Ignore bot messages
    if message.author.bot:
        return

    msg_logging.log_message(message)
    
    await bot.process_commands(message)

@bot.hybrid_command()
async def random_msg(ctx: commands.Context):
    msg = msg_logging.get_random_msg(ctx.guild.id,ctx.channel.id)
    if msg:
        response = f"{msg['content']}"
        if msg['attachments']:
            for attachment_url in msg['attachments']:
                response += attachment_url

        await ctx.send(response)
    else:
        await ctx.send("No messages logged for this channel yet.")


@bot.hybrid_command()
async def ping(ctx: commands.Context):
    await ctx.send('pong')

@bot.hybrid_command()
@app_commands.checks.has_permissions(manage_guild=True)
async def clear_all_msg(ctx: commands.Context):
    msg_logging.clear_all(ctx.guild.id)
    await ctx.send("Cleared")

@bot.hybrid_command()
@app_commands.checks.has_permissions(manage_guild=True)
async def clear_channel_msg(ctx: commands.Context, channel: TextChannel):
    msg_logging.clear_channel(ctx.guild.id, channel.id)
    await ctx.send("Cleared")

@bot.hybrid_command()
@app_commands.checks.has_permissions(manage_guild=True)
async def togglechannel(ctx: commands.Context, channel: TextChannel, active: bool):
    status = settings.toggle_channel(ctx.guild.id, channel.id, active)
    await ctx.send(status)


@bot.hybrid_command()
async def gen(ctx: commands.Context, channel: TextChannel = None):
    if channel == None:
        channel = ctx.channel
    txt = generation.gen_message(ctx.guild.id, channel.id)
    if txt == None:
        await ctx.send("Error! (maybe not enough data idk)")
        return
    await ctx.send(txt)

@bot.hybrid_command()
async def gen_all(ctx: commands.Context):
    txt = generation.gen_message_all(ctx.guild.id)
    if txt == None:
        await ctx.send("Error! (maybe not enough data idk)")
        return
    await ctx.send(txt)



# STEP 5: MAIN ENTRY POINT
def main():
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()


