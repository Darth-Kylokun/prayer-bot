from discord.ext.commands import Cog, Bot, command, Context
from discord.ext.commands.core import has_guild_permissions, has_permissions
from discord.ext.commands.errors import BadArgument, CommandError, MissingPermissions, MissingRequiredArgument, NoPrivateMessage
from discord.mentions import AllowedMentions
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.session import sessionmaker
from database import Entitys, Prayers, Prefixes, async_engine
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy.future import select
from discord import Embed
from datetime import datetime

class Commands(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
        self.am = AllowedMentions()
        self.am.replied_user = False

    @command()
    async def entities(self, ctx: Context):
        async with self.session() as s:
            entity_stmt = select(Entitys).where(Entitys.user_id == ctx.author.id)

            res = await s.execute(entity_stmt)

            entity_obj = res.scalars()

            embed = Embed(title="Entities", color=0x990000)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            for entity in entity_obj:
                embed.add_field(name=f"> {entity.name}", value="\u200b", inline=False)
            
            embed.timestamp = datetime.utcnow()

            await ctx.send(embed=embed)

    @command()
    async def prayers(self, ctx: Context, entity: str):
        async with self.session() as s:
            entity_stmt = select(Entitys).where(Entitys.name == entity).where(Entitys.user_id == ctx.author.id).options(selectinload(Entitys.ps))

            res = await s.execute(entity_stmt)
            
            entity_obj = res.scalars().first()

            try:
                prayers = entity_obj.ps

                if len(prayers) == 0:
                    await ctx.reply(f"{entity}, has no prayers associated with it.", allowed_mentions=self.am)
                    return

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ('⬅️', '➡️')
                
                pointer = 0
                embed = Embed(title=f"Prayers for {entity}", color=0x990000)
                print(entity_obj.image)
                if entity_obj.image is not None:
                    embed.set_thumbnail(url=entity_obj.image)
                embed.add_field(name=f"Prayer {pointer + 1}", value=f"{prayers[pointer].text}", inline=False)
                embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.timestamp = datetime.utcnow()
                try:
                    embed.add_field(name=f"Prayer {pointer + 2}", value=f"{prayers[pointer+1].text}", inline=False)
                except:
                    pass
                message = await ctx.send(embed=embed)
                if len(prayers) > 2:
                    await message.add_reaction('➡️')
                else:
                    return

                while 1:
                        try:
                            reaction, _ = await self.bot.wait_for('reaction_add', timeout=30, check=check)

                            if reaction.emoji == '➡️':
                                pointer += 2
                            elif reaction.emoji == '⬅️':
                                pointer -= 2

                            await message.clear_reactions()

                            if pointer >= 2:
                                await message.add_reaction('⬅️')
                            if len(prayers) >= pointer+3:
                                await message.add_reaction('➡️')

                            e_embed = Embed(title=f"Prayers for {entity}", color=0x990000)
                            embed.set_thumbnail(url=entity_obj.image)
                            e_embed.add_field(name=f"Prayer {pointer + 1}", value=f"{prayers[pointer].text}", inline=False)
                            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                            embed.timestamp = datetime.utcnow()
                            try:
                                e_embed.add_field(name=f"Prayer {pointer + 2}", value=f"{prayers[pointer+1].text}", inline=False)
                            except:
                                pass
                           
                            await message.edit(embed=e_embed)
                        except asyncio.TimeoutError:
                            return
            except AttributeError:
                await ctx.reply(f"{entity} not found", allowed_mentions=self.am)
            
    @prayers.error
    async def addentity_error(self, ctx: Context, error: CommandError):
        if isinstance(error, MissingRequiredArgument):
            await ctx.reply("Missing argument\n> prayers <name>", allowed_mentions=self.am)

    @command()
    async def updateimage(self, ctx: Context, entity: str):
        try:
            image = ctx.message.attachments[0].url
        except:
            await ctx.reply("Please attach an image", allowed_mentions=self.am)
            return
        
        async with self.session() as s:
            async with s.begin():
                stmt = select(Entitys).where(Entitys.name == entity).where(Entitys.user_id == ctx.author.id)

                res = await s.execute(stmt)

                res.scalars().first().image = image

                await s.commit()
        
        await ctx.send(f"Successfully updated image for {entity}")

    @updateimage.error
    async def updateimage_error(self, ctx: Context, error: CommandError):
        if isinstance(error, MissingRequiredArgument):
            await ctx.reply("Missing argument\n> updateimage <entity>", allowed_mentions=self.am)

    @command()
    async def addprayer(self, ctx: Context, entity: str, *, prayer: str):
        async with self.session() as s:
            async with s.begin():
                ent_stm = select(Entitys).where(Entitys.name == entity).where(Entitys.user_id == ctx.author.id)

                res = await s.execute(ent_stm)
                
                entity_id = 0

                try:
                    entity_id = res.scalars().first().id
                except AttributeError:
                    await ctx.reply(f"{entity} not found", allowed_mentions=self.am)
                    return

                prayer = Prayers(text=prayer, e_id=entity_id)

                s.add(prayer)
                await s.commit()

                await ctx.send(f"Added prayer for {entity}")

    @addprayer.error
    async def addentity_error(self, ctx: Context, error: CommandError):
        if isinstance(error, MissingRequiredArgument):
            await ctx.reply("Missing argument\n> addprayer <name> <prayer>", allowed_mentions=self.am)

    @command()
    async def addentity(self, ctx: Context, entity: str):
        image = None

        try:
            image = ctx.message.attachments[0].url
        except:
            pass

        new_entity = Entitys(name=entity, image=image, user_id=ctx.author.id)

        async with self.session() as s:
            async with s.begin(): 
                stmt = select(Entitys).where(Entitys.name == new_entity.name).where(Entitys.user_id == ctx.author.id)

                res = await s.execute(stmt)

                if res.scalars().first() is None:
                    s.add(new_entity)

                    await s.commit()
                    await ctx.send(f"Added entity {entity}")
                else:
                    await ctx.reply(f"{entity} already exist", allowed_mentions=self.am)

    @addentity.error
    async def addentity_error(self, ctx: Context, error: CommandError):
        if isinstance(error, MissingRequiredArgument):
            await ctx.reply("Missing argument\n> addentity <name>", allowed_mentions=self.am)

    @command()
    async def updatename(self, ctx: Context, old_entity: str, new_entity: str):
        async with self.session() as s:
            async with s.begin():
                stmt = select(Entitys).where(Entitys.name == old_entity).where(Entitys.user_id == ctx.author.id)
                check_stmt = select(Entitys).where(Entitys.name == new_entity).where(Entitys.user_id == ctx.author.id)

                res = await s.execute(check_stmt)

                if res.scalars().first() is not None:
                    await ctx.reply(f"You already have an entity named {new_entity}", allowed_mentions=self.am)
                    return

                res = await s.execute(stmt)
                try:
                    res.scalars().first().name = new_entity
                except AttributeError:
                    await ctx.reply(f"{old_entity} not found", allowed_mentions=self.am)
                    return

                await s.commit()
        
        await ctx.send(f"Updated {old_entity} to {new_entity}")

    @updatename.error
    async def updatename_error(self, ctx: Context, error: CommandError):
        if isinstance(error, MissingRequiredArgument):
            await ctx.reply("Missing argument\n> updatename <old_name> <new_name>", allowed_mentions=self.am)

    @command()
    async def removeprayer(self, ctx: Context, entity: str, id: int):
        stmt = select(Entitys).where(Entitys.name == entity).where(Entitys.user_id == ctx.author.id).options(selectinload(Entitys.ps))
        
        async with self.session() as s:
            async with s.begin():
                res = await s.execute(stmt)

                entity_obj = res.scalars().first()

                try:
                    await s.delete(entity_obj.ps[id-1])
                except AttributeError:
                    await ctx.reply(f"{entity} not found", allowed_mentions=self.am)
                    return
                except IndexError:
                    await ctx.reply(f"{entity} has no prayers associated with it", allowed_mentions=self.am)
                    return

                await s.commit()

        await ctx.send("Removed prayer")
    
    @removeprayer.error
    async def removeprayer_error(self, ctx: Context, error: CommandError):
        if isinstance(error, BadArgument):
            await ctx.reply("Invalid ID passed", allowed_mentions=self.am)
        elif isinstance(error, MissingRequiredArgument):
            await ctx.reply("Missing argument\n> removeprayer <name> <id>", allowed_mentions=self.am)

    @command()
    async def removeentity(self, ctx: Context, entity: str):
        async with self.session() as s:
            async with s.begin():
                stmt = select(Entitys).where(Entitys.name == entity).where(Entitys.user_id == ctx.author.id).options(selectinload(Entitys.ps))

                res = await s.execute(stmt)

                entity_obj = res.scalars().first()
                try:
                    for prayer in entity_obj.ps:
                        await s.delete(prayer)

                    await s.delete(entity_obj)
                except:
                    await ctx.reply(f"{entity} not found", allowed_mentions=self.am)
                    return

                await s.commit()
        await ctx.send(f"{entity} was removed")

    @removeentity.error
    async def removeentity_error(self, ctx: Context, error: CommandError):
        if isinstance(error, MissingRequiredArgument):
            await ctx.reply("Missing argument\n> removeentity <name>", allowed_mentions=self.am)

    @command()
    @has_guild_permissions(administrator=True)
    async def changeprefix(self, ctx: Context, new_prefix: str):
        async with self.session() as s:
            async with s.begin():
                stmt = select(Prefixes).where(Prefixes.server_id == ctx.guild.id)
                res = await s.execute(stmt)

                res.scalars().first().prefix = new_prefix

                await s.commit()

        await ctx.send(f"Succefully change prefix to {new_prefix}")

    @changeprefix.error
    async def changeprefix_error(self, ctx: Context, error: CommandError):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You are missing the permssion for 'administrator'", allowed_mentions=self.am)
        elif isinstance(error, NoPrivateMessage):
            await ctx.reply("You can only change the prefix in servers", allowed_mentinos=self.am)
        elif isinstance(error, MissingRequiredArgument):
            await ctx.reply("Missing argument\n> changeprefix <new_prefix>", allowed_mentions=self.am)

def setup(bot: Bot):
    bot.add_cog(Commands(bot))
