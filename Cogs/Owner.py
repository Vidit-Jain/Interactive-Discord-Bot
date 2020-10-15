import discord
from discord.ext import commands
from discord.utils import get
from Resource.aliases import aliases
import os

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def cog_check(self, ctx):
        'Check if user is bot owner'

        return await self.bot.is_owner(ctx.author)


    def cogPresent(self, extension):
        'To check if the file is present in the cog'

        return extension + '.py' in os.listdir('./Cogs')


    def _load(self, extension):
        'To load the Cog'

        if extension in aliases.keys():
            extension = aliases[extension]
        
        if self.cogPresent(extension):
            try:
                self.bot.load_extension(f'Cogs.{extension}')
                return f'You have successfully added the {extension} cog'
            except:
                return f'The {extension} Cog is already loaded'

        else:
            return 'No such Cog exists'


    @commands.command(aliases = ['L'])
    async def load(self, ctx, extension):
        'To load Cogs'  

        await ctx.send(self._load(extension))

    
    def _unload(self, extension):
        'To unload the Cog'

        if extension in aliases.keys():
            extension = aliases[extension]
        
        if self.cogPresent(extension):
            if (extension != 'Owner'):
                try:
                    self.bot.unload_extension(f'Cogs.{extension}')
                    return f'You have successfully unloaded the {extension} cog.'
                except:
                    return f'The {extension} Cog is already unloaded'
            else:
                return 'You cannot unload the Owner cog'
        else:
            return 'No such Cog exists'
        

    @commands.command(aliases = ['UL'])
    async def unload(self,ctx,extension):
        'To unload Cogs'

        await ctx.send(self._unload(extension))


    @commands.command(aliases = ['RL'])
    async def reload(self,ctx,extension):
        'To reload Cogs'

        if extension in aliases.keys():
            extension = aliases[extension]
        
        if self.cogPresent(extension):
            self._unload(extension)
            self._load(extension)
            await ctx.send("You have successfully reloaded the Cog")
        else:
            await ctx.send("No such Cog exists")
            

def setup(bot):
    bot.add_cog(Owner(bot))