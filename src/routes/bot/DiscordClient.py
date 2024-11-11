import discord

class DiscordClient(discord.Client):
    ready = False
    
    async def on_ready(self):
        self.ready = True
        print(f'[INFO] Discord: logged in as {self.user}')
        
    def is_ready(self):
        return self.ready