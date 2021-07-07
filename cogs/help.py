from discord.ext.commands import Cog, Bot, command, Context
from discord import Embed
from datetime import datetime

class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['h'])
    async def help(self, ctx: Context):
        embed = Embed(title="Prayer Commands", color=0x990000, description="Prayer bot allows you to store different prayers dedicated to different entities.")

        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="> help | alias h", value="Help and documentation for prayer bot", inline=False)
        embed.add_field(name="> addentity <entity_name> | alias ae", value="Creates an entity and you can also attach an image that will then be associated with that entity", inline=False)
        embed.add_field(name="> updatename <old_entity_name> <new_entity_name> | alias un", value="Changes an entitys name", inline=False)
        embed.add_field(name="> updateimage <entity_name> | alias ui", value="Allows you to add or update an image for an entity", inline=False)
        embed.add_field(name="> addprayer <entity_name> <prayer> | alias ap", value="Stores a prayer dedicated to an entity", inline=False)
        embed.add_field(name="> prayers <entity_name> | alias p", value="Shows stored prayers for that entity and gives the prayers id along with them", inline=False)
        embed.add_field(name="> entities | alias e", value="Shows all entities you have added", inline=False)
        embed.add_field(name="> removeprayer <entity_name> <id> | alias rp", value="Removes a prayer from an entity and the rest of the prayer IDs might change", inline=False)
        embed.add_field(name="> removeentity <entity_name> | alias re", value="Removes an entity", inline=False)
        embed.add_field(name="> changeprefix <new_prefix> | alias cp", value="Changes the prefix in a server. The default prefix/dm prefix is !!", inline=False)
        embed.add_field(name="**WARNING**", value="If an entity has name that involves two words you must encapsulate the name in quotation marks ex. \"prayer bot\" or you can add a underscore to represent a space ex. prayer_bot", inline=False)
        embed.add_field(name="Inviet link for bot:", value="[INVITE](https://discord.com/oauth2/authorize?client_id=754848887323361350&permissions=76864&scope=bot)", inline=False)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(Help(bot))