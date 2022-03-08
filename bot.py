from urllib import response
import nextcord
from decouple import config
import nextcord
from nextcord import client
from nextcord.ext import commands
import os

from utils.database import pc_random, u_insert

KEY = config('KPOP_TOKEN')
intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '!', intents=intents,help_command=None)

def log(msg):
    """
    Logs message to files
    """
    with open('log.txt', 'a') as f:
        print(msg, file=f)

class Confirm(nextcord.ui.View):
    def __init__(self,photocard,id):
        super().__init__(timeout=60)
        self.value = None
        self.pc = photocard
        self.id = id

    #async def on_timeout(self):
    #    await self.message.edit(embed=self.summary, view=None)

    @nextcord.ui.button(label="Claim", style=nextcord.ButtonStyle.blurple)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.id == interaction.user.id:
            log(f"{self.id} Claimed PC: {self.pc}")
            #insert into database
            await interaction.response.send_message("You claimed: RM! Love Yourself: Her (O) Card", ephemeral=True)
        else: 
            log(f"{interaction.user.id} Tried to Claim PC: {self.pc} from {self.id}")
            await interaction.response.send_message("This is not your card to claim!",ephemeral=True)
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Throw away", style=nextcord.ButtonStyle.blurple)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.id == interaction.user.id:
            log(f"{self.id} Denied PC: {self.pc}")
            await interaction.response.send_message("RIP",ephemeral=True)
        else:
            log(f"{interaction.user.id} Tried to Deny PC: {self.pc} from {self.id}")
            await interaction.response.send_message("This is not your card to cancel!",ephemeral=True)
        self.value = False
        self.stop()


def is_it_admin(ctx):
    if ctx.author.id == 219274325058912257:
        return True

@client.command(brief='Load cogs through bot.', description='Load cogs that add different features manually.')
@commands.check(is_it_admin)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} Successfully loaded.')

@client.command(brief='Unload cogs through bot.', description='Unload cogs that add different features manually.')
@commands.check(is_it_admin)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} Successfully unloaded.')


@client.group(name="help")
async def help(ctx):
    embed=nextcord.Embed(title=f"Help Command",description='The prefix for commands is "!" but you already knew that ;) ', color=0xFF36ED)
    embed.set_author(name="Hyunjin", icon_url="https://cdn.discordapp.com/attachments/834497419479089222/943259876073824266/V__LY_Her_-_ver__V.jpg")
    embed.add_field(name="help", value="The help command. Idk you're looking at it.",inline=False)
    embed.add_field(name="drop", value="Get a random photocard.",inline=False)
    #embed.set_thumbnail(url="https://cdn.nextcordapp.com/attachments/844693985653424148/898980600206225408/Spotify_Icon_RGB_Green.png")
    #embed.set_image(url="https://i.scdn.co/image/ab6765630000ba8a41f6be3eea7a43f13068d5e9")
    await ctx.send(embed=embed)


@client.command()
#@commands.cooldown(1, 60, commands.BucketType.user)
async def drop(ctx):
    user = ctx.author.id
    print(type(user))
    photocard = pc_random()
    embed=nextcord.Embed(title=f"A **{photocard[0]}** has been dropped",description="", color=0xFF36ED)
    embed.set_author(name="Hyunjin", icon_url="https://cdn.discordapp.com/attachments/834497419479089222/943259876073824266/V__LY_Her_-_ver__V.jpg")
    embed.set_image(url=photocard[1])
    view = Confirm(photocard[0],int(user))
    await ctx.send(embed=embed, view=view)
    await view.wait()

@client.command()
async def register(ctx):
    u_insert(ctx.author.id)
    await ctx.send('Thank you for joining! Have fun!')

@client.command()
async def leaveg(ctx, *, guild_name):
    guild = nextcord.utils.get(client.guilds, name=guild_name) # Get the guild by name
    if guild is None:
        print("No guild with that name found.") # No guild found
        return
    await guild.leave() # Guild found
    await ctx.send(f"I left: {guild.name}!")


#Load all cogs in the cog folder.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"{filename} Has Been Loaded" )

try:
    client.run(KEY)
except:
    print('There was an error with running the bot.')