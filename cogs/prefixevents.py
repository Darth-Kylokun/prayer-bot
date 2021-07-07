from discord.ext.commands import Cog, Bot
from sqlalchemy.sql.expression import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from database import Prefixes, async_engine
from discord import Activity, ActivityType
from itertools import cycle
from discord.ext import tasks

class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
        self.cycle = None
        self.ready = False

    @Cog.listener()
    async def on_ready(self):
        if not self.ready:
            self.cycle = cycle([f"{len(self.bot.guilds)} servers", "!!help command"])

            self.change.start()
            self.update_cycle.start()

            print(f"Connected to bot: {self.bot.user.name}")
            print(f"Bot ID: {self.bot.user.id}")

            self.ready= True

    @Cog.listener()
    async def on_resumed(self):
        self.change.start()
        self.update_cycle.start()

        print("Reconnected")

    @Cog.listener()
    async def on_guild_join(self, guild):
        async with self.session() as s:
            async with s.begin():
                prefix = Prefixes(prefix="!!", server_id=guild.id)
                s.add(prefix)
                await s.commit()

    @Cog.listener()
    async def on_guild_remove(self, guild):
        async with self.session() as s:
            async with s.begin():
                stmt = select(Prefixes).where(Prefixes.server_id == guild.id)
                res = await s.execute(stmt)
                await s.delete(res.scalars().first())
                await s.commit()

    @Cog.listener()
    async def on_disconnect(self):
        self.change.cancel()
        self.update_cycle.cancel()
        print("Disconnected")

    @tasks.loop(minutes=3)
    async def change(self):
        await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=next(self.cycle)))

    @tasks.loop(minutes=30)
    async def update_cycle(self):
        self.cycle = cycle([f"{len(self.bot.guilds)} servers", "!!help command"])
        # This is somewhat bad but damnt i want the amount of guilds to be accurate to an extent


def setup(bot: Bot):
    bot.add_cog(Events(bot))
