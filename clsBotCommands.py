from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import telegram

class clsBotCommands:
    @staticmethod
    async def __SendMessageWithoutButtons(update:Update,Text: str, ReplyToMessage:bool = False) -> bool:
        
        if ReplyToMessage:
            await update.message.reply_text(parse_mode='Markdown',text=Text, reply_to_message_id= update.message.message_id)
            try:
                 return True
            except:
                return False
        
        try:
            await update.message.reply_text(parse_mode='Markdown',text=Text)
            return True
        except:
            return False  
    @staticmethod
    async def SendMessageTxt(update:Update,Text: str, ReplyToMessage:bool = False, ButtonsList:list = []) -> bool:
        
        if not ButtonsList: return await clsBotCommands.__SendMessageWithoutButtons(update,Text, ReplyToMessage)
        
        if ReplyToMessage:
            try:
                await update.message.reply_text(parse_mode='Markdown',text= Text, reply_to_message_id=update.message.message_id, reply_markup=InlineKeyboardMarkup(ButtonsList))
                return True
            except:return False

        try:
            await update.message.reply_text(parse_mode='Markdown',text=Text, reply_markup=InlineKeyboardMarkup(ButtonsList))
            return True
        except:return False

    @staticmethod
    async def __SendPhotoWithoutButtons(update:Update, Photo:str, Caption:str, ReplyToMessage:bool = False) ->bool:
        if not ReplyToMessage :
            try:
                await update.message.reply_photo(photo=Photo, caption=Caption)
                return True
            except: return False        
        
        
        try:
            await update.message.reply_photo(photo=Photo, caption=Caption, reply_to_message_id=update.message.message_id)
            return True
        except: return False
    @staticmethod
    async def SendPhoto(update:Update,Photo:str, Caption:str, ReplyToMessage:bool = False, ButtonsList:list = [])->bool:
        if not ButtonsList: return await clsBotCommands.__SendPhotoWithoutButtons(update=update,Photo=Photo, ReplyToMessage=ReplyToMessage, Caption=Caption)
        
        if ReplyToMessage:
            try:
                await update.message.reply_photo(parse_mode='Markdown',photo=Photo, caption=Caption, reply_to_message_id=update.message.message_id, reply_markup=InlineKeyboardMarkup(ButtonsList))
                return True
            except:return False

        try:
            await update.message.reply_photo(photo=Photo, caption=Caption, reply_markup=InlineKeyboardMarkup(ButtonsList),parse_mode='Markdown')
            return True
        except:return False


