from discord.ext.commands import Cog, Bot
from sqlalchemy.sql.expression import select
from database import coro_session, Prefixes

class PrefixEvents(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.session = coro_session

    @Cog.listener()
    async def on_guild_join(self, guild):
        async with self.session() as s:
            async with s.begin():
                prefix = Prefixes(prefix="!!", server_id=guild.id)
                s.add(prefix)
                await s.commit()

    @Cog.listener()
    async def on_guild_leave(self, guild):
        async with self.session() as s:
            async with s.begin():
                stmt = select(Prefixes).where(Prefixes.server_id == guild.id)
                res = await s.execute(stmt)
                await s.remove(res.scalars().first())
                await s.commit()

def setup(bot: Bot):
    bot.add_cog(PrefixEvents(bot))
