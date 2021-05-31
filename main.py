import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

def main():
    load_dotenv()

    Bot = commands.Bot(command_prefix="!!")
    Bot.remove_command("help")

    for f in os.listdir('./cogs'):
        if f.endswith('.py'):
            Bot.load_extension(f'cogs.{f[:-3]}')
    
    token = os.environ['TOKEN']

    Bot.run(token)


if __name__ == '__main__':
    main()
