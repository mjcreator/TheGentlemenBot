import logging
import traceback
from disnake.ext import commands
import disnake
from os.path import dirname, isfile, relpath, join
import glob
import config

class GentlemenBot(commands.Bot):
    def __init__(self):
        allowedMentions = disnake.AllowedMentions(everyone=False,roles=True,users=True)
        intents = disnake.Intents(
            guilds = True,
            members = True,
            bans = True,
            emojis = True,
            voice_states = True,
            messages = True,
            reactions = True
        )

        super().__init__(
            command_prefix='/',
            allowedMentions=allowedMentions,
            intents=intents,
            enable_debug_events=True,
            test_guilds=config.testServers,
            sync_permissions=True
        )

        self.client_id  = config.client_id
        self.log = logging.getLogger(type(self).__name__)

        self.add_cog(BotManager(self, self.log))

        self.loadedExtentions = []

        for ext in config.cogs:
            try:
                self.log.info(f"loading extension {ext}")
                self.load_extension(ext)
                self.loadedExtentions.append(ext)

            except Exception:
                self.log.exception(f"Error loading {ext}:")
                traceback.print_exc()

    async def on_ready(self):
        self.log.info("Bot Running")
        if ("botActivity" in config.__dict__ and config.botActivity):
            activity = disnake.Game(name=config.botActivity)
            await self.change_presence(activity=activity)

    def run(self):
        try:
            super().run(config.token, reconnect=True)
        finally:
            pass

class BotManager(commands.Cog):
    def __init__(self, bot : commands.Bot, logger : logging.Logger):
        self.bot = bot
        self.log = logger

    @commands.slash_command(default_permission=False)
    @commands.is_owner()
    @commands.guild_permissions(guild_id=916230367004987422,users={528674907618410516:True})
    async def reloadExt(self, inter : disnake.ApplicationCommandInteraction, ext : str):
        '''
        reloads a bot extention.
        '''
        if(ext in self.bot.loadedExtentions):
            try:
                await inter.response.defer(ephemeral=True)
                self.log.info(f"reloading extension {ext}")
                self.bot.reload_extension(ext)
                await inter.edit_original_message(content=f"Successfully reloaded {ext}!")
            except Exception:
                self.log.exception(f"Error loading {ext}:") 
                error = traceback.format_exc()
                await inter.edit_original_message(content=f"Failed to reloaded {ext} with exception ```\n{error}```")
        else:
            await inter.send(content=f"{ext} was not found.", ephemeral=True)
    
    @commands.slash_command(default_permission=False)
    @commands.is_owner()
    @commands.guild_permissions(guild_id=916230367004987422,users={528674907618410516:True})
    async def loadExt(self, inter : disnake.ApplicationCommandInteraction, ext : str):
        '''
        loads a bot extention.
        '''
        if(ext in self.getModules()):
            try:
                await inter.response.defer(ephemeral=True)
                self.log.info(f"load extension {ext}")
                self.bot.load_extension(ext)
                self.bot.loadedExtentions.append(ext)
                await inter.edit_original_message(content=f"Successfully loaded {ext}!")
            except Exception:
                self.log.exception(f"Error loading {ext}:") 
                error = traceback.format_exc()
                await inter.edit_original_message(content=f"Failed to loaded {ext} with exception ```\n{error}```")
        else:
            await inter.send(content=f"{ext} was not found.", ephemeral=True)

    @commands.slash_command(default_permission=False)
    @commands.is_owner()
    @commands.guild_permissions(guild_id=916230367004987422,users={528674907618410516:True})
    async def unloadExt(self, inter : disnake.ApplicationCommandInteraction, ext : str):
        '''
        reloads a bot extention.
        '''
        if(ext in self.bot.loadedExtentions):
            try:
                await inter.response.defer(ephemeral=True)
                self.log.info(f"unloading extension {ext}")
                self.bot.unload_extension(ext)
                self.bot.loadedExtentions.remove(ext)
                await inter.edit_original_message(content=f"Successfully unloaded {ext}!")
            except Exception:
                self.log.exception(f"Error unloading {ext}:") 
                error = traceback.format_exc()
                await inter.edit_original_message(content=f"Failed to unloading {ext} with exception ```\n{error}```")
        else:
            await inter.send(content=f"{ext} was not found.", ephemeral=True)
    
    @commands.slash_command(default_permission=False)
    @commands.is_owner()
    @commands.guild_permissions(guild_id=916230367004987422,users={528674907618410516:True})
    async def setActivity(self, inter : disnake.ApplicationCommandInteraction, act : str = None):
        '''
        Sets the text of the bot activity.
        '''
        activity = None
        if(act):
            activity = disnake.Game(name=act)
        await self.bot.change_presence(activity=activity)
        await inter.send(content=f"Set activity to \"{act}\".", ephemeral=True)

    @reloadExt.autocomplete('ext')
    @unloadExt.autocomplete('ext')
    async def autoCompleteCogs(self, inter : disnake.CommandInteraction, user_input: str):
        return [cog for cog in self.bot.loadedExtentions if cog.startswith(user_input)]

    def getModules(self):
        modules = []
        directory = join(dirname(__file__), "cogs")
        for module in glob.glob(join(directory , "*.py")):
            if not isfile(module):
                continue
            name = ""
            try:
                name = relpath(module,directory)[:-3]
            except ValueError:
                continue
            if(name):
                modules.append(f"cogs.{name}")
        return modules

    @loadExt.autocomplete('ext')
    async def autoCompleteUnloadedCogs(self, inter : disnake.CommandInteraction, user_input: str):
        return [cog for cog in self.getModules() if user_input in cog]