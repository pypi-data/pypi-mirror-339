from aiogram import Bot, Dispatcher, types
import asyncio

class EasyBot:
    def __init__(self, token: str):
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot)
        
    def command(self, name: str):
        """Decorator for commands"""
        return self.dp.message_handler(commands=[name])
        
    def run(self):
        """Starting bot"""
        asyncio.run(self.dp.start_polling())
