import nextcord
from nextcord.ext import commands,tasks


class startup(commands.Cog, nextcord.Client,):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()

    @tasks.loop(seconds=1, reconnect=True, count=1)
    async def check(self): 
        await self.client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="!help"))
        
try:
    def setup(client):
        client.add_cog(startup(client))
except:
    print('There was an error starting the Commands Cog')
