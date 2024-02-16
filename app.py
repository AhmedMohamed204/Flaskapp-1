
from telegram import Bot
from telegram.ext import Updater
from PresentationLayer import clsBot
BOT_TOKEN:str = "TOKEN"
def main():
    bot = clsBot(BOT_TOKEN)
    bot.Run()




print("app is running ")
main()
