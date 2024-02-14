
from telegram import Bot
from telegram.ext import Updater
from PresentationLayer import clsBot
import asyncio
from server import server
BOT_TOKEN:str = "6499575874:AAF1JWagbmy7trIphPNf9I5tZMFfrz3APDE"
def main():
    bot = clsBot(BOT_TOKEN)
    bot.Run()




print("app is running ")
server()
main()
