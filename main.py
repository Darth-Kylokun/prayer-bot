import os
from discord.ext import commands
from database import session, Prefixes
from discord import Intents

def get_prefix(_bot, message):
    try:
        return session.query(Prefixes).filter_by(server_id=message.guild.id).one().prefix
    except:
        return "!!"

def main():
    intents: Intents = Intents.default()

    Bot = commands.Bot(command_prefix=get_prefix, intents=intents)
    Bot.remove_command("help")

    for f in os.listdir('./cogs'):
        if f.endswith('.py'):
            Bot.load_extension(f'cogs.{f[:-3]}')

    token = os.environ['TOKEN']

    Bot.run(token)


if __name__ == '__main__':
    main()
