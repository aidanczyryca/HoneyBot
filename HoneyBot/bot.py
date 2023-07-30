# Imports
from sensitive import TOKEN
import discord
import responses
import logging
import logging.handlers
import sys
from discord.ext import commands
from colorama import init, Fore, Back, Style
init(autoreset=True)

# Accepting messages
async def send_message(message, user_message, is_private):
    try:
        user_message = str(message.guild.id) + '|' + str(message.guild) + '|' + str(message.author) + '|' + user_message

        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# What to do with those messages
def run_discord_bot():

    # Declare intents
    client = discord.Client(intents = discord.Intents.all())

    # Logging : Creates logger named 'discord' and logs Verbose except for HTTP requests. 
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logging.getLogger('discord.http').setLevel(logging.INFO)

    # Formats the log files
    handler = logging.handlers.RotatingFileHandler(
        filename='discord_events.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 7 files
    )

    # Formats the log entries
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Activiation message
    @client.event
    async def on_ready():
        #await tree.sync() # await tree.sync(guild=discord.Object(id=Your guild id))
        print(Fore.CYAN + f'{client.user} is now running!\a')


    # Infinite loop prevention
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        # Declaring message variables
        username = str(message.author)
        user_message = str(message.content)
        channel_name = str(message.channel)
        channel_id = message.channel.id
        guild_name = str(message.guild)
        guild_id = message.guild.id
        
        print(Fore.BLUE + f'{username} said: "{user_message}" in channel: {channel_name} ({channel_id}) from guild: {guild_name} ({guild_id})')

        # Handles whether the message is private or public
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

        # is a part of the valley
        if guild_id == 310228470229893121:
            # Handles @ reactions
            if '@everyone' in user_message:
                await message.add_reaction('<:monkMultiPing:595700898953428996>')
            elif '@' in user_message:
                await message.add_reaction('<:monkPing:538627236895391774>')
        # !!! (lies) 

        if user_message == '!shutdown' & username == 'tropicalmango':
            # send goodbye message
            client.close()
            sys.exit()

        
    @client.event
    async def on_raw_reaction_add(payload):
        # is a part of the valley
        if payload.guild_id == 310228470229893121:
            if str(payload.emoji) == '<:freeman_point:782805318911787059>':
                try:
                    freeman_file = open('HoneyBot/Logs/freeman_tracker.txt', 'a')
                except:
                    freeman_file = open('/home/aidan/Documents/GitHub/HoneyBot/HoneyBot/Logs/freeman_tracker.txt', 'a')
                freeman_file.write(str({payload.member.id})[1:-1] + '\n') # was (user)
                freeman_file.close()


    @client.event
    async def on_raw_member_leave(payload):
        print('Someone left a server.')
        #await client.

    # custom commands
    bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())

    @bot.command(name = "tester", description = "My first application Command") #, guild=discord.Object(id=12417128931)Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
    async def tester(ctx, message):
        print('detected')
        await ctx.send(message)


    client.run(TOKEN, log_handler=None)



