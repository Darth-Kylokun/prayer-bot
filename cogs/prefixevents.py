from discord.ext.commands import Cog, Bot
from sqlalchemy.sql.expression import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from database import Prefixes, async_engine

class PrefixEvents(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession) # This inly works because coro_session has already been awaited in another cog. Why does this work i have no idea

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

def setup(bot: Bot):
    bot.add_cog(PrefixEvents(bot))
