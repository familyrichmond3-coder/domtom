import discord
import threading

_bot = None

def start(token):
    global _bot
    intents = discord.Intents.default()
    intents.message_content = True
    _bot = discord.Client(intents=intents)
    
    @_bot.event
    async def on_ready():
        print(f'Discord бот {_bot.user} готов!')

    def run():
        _bot.run(token)
        
    threading.Thread(target=run, daemon=True).start()

запустить = start