
import telegram

from QuestionsBuesnissLayer import clsQuestion
from UsersBusinessLayer import clsUser
from telegram import  Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.ext import filters,Application, CallbackQueryHandler, Updater, CommandHandler, MessageHandler, CallbackContext
from clsAdminCommands import clsAdminCommands
from clsBotCommands import clsBotCommands
from clsQuiz import clsQuiz

    
class clsBot:
    def __init__(self, BOT_TOKEN) -> None:
        self.App = Application.builder().token(BOT_TOKEN).build()
        self.bot = telegram.Bot(BOT_TOKEN) 
        
        
    async def OnClickButton(self,update: Update, context: CallbackContext):
        ButtonName = update.callback_query.data
        if ButtonName == "رياضيات": return await clsQuiz.SendQuestion(1,update,context)
        if ButtonName == "فيزياء": return await clsQuiz.SendQuestion(2,update,context)
        if ButtonName == "كيمياء": return await clsQuiz.SendQuestion(3,update,context)
        if ButtonName == "احياء": return await clsQuiz.SendQuestion(4,update,context)
        if ButtonName == "عشوائي": return await clsQuiz.SendQuestion(-1,update,context)
        if ButtonName == "ا": return await clsQuiz.PerformUserAnswer(update,context)
        if ButtonName == "ب": return await clsQuiz.PerformUserAnswer(update,context)
        if ButtonName == "ج": return await clsQuiz.PerformUserAnswer(update,context)
        if ButtonName == "د": return await clsQuiz.PerformUserAnswer(update,context)
        if ButtonName == "Main": return await clsQuiz.Main(update,context)
        if ButtonName == "ShowExplain": return await clsAdminCommands.ShowExplainOfQuestion(update,context)
        if ButtonName == "ShowQuestion": return await clsAdminCommands.ShowQuestionAfterExpalin(update,context)
    def __GetUserData(self,User:clsUser)->str:
        
        return f"{ '*Admin*' if User.Permissions == -1 else ''}\n*User Id*: {User.UserID}\n*Total Answers*: {User.TotalAnswers}\n*Total Right Answers*: {User.TotalRightAnswers}"
    async def Command_Me(self,update: Update, context: CallbackContext):
        UserID = update.message.from_user.id
        User = clsUser.Find(UserID)
        Text:str = self.__GetUserData(User)
        return await clsBotCommands.SendMessageTxt(update,Text=Text, ReplyToMessage=True)

    def Run(self):
        print("Bot has been started !")
        app = self.App
        app.add_handler(CommandHandler('start', self.Start))
        app.add_handler(CommandHandler('me', self.Command_Me))
        app.add_handler(CommandHandler('help', self.HelpCommand))
        app.add_handler(CommandHandler(['dashboard', 'd'], clsAdminCommands.Dashboard))
        app.add_handler(CommandHandler('chat', clsAdminCommands.SendChatID))
        app.add_handler(CommandHandler('add', clsAdminCommands.AddQuestion))
        app.add_handler(CommandHandler('show', clsAdminCommands.ShowQuestion))
        app.add_handler(CommandHandler('delete', clsAdminCommands.DeleteQuestion))
        app.add_handler(CommandHandler('update', clsAdminCommands.UpdateQuestion))
        app.add_handler(CommandHandler('send', self.SendMessageToUser))
        app.add_handler(CommandHandler('all', self.SendMessageToAllUsers))
        app.add_handler(CommandHandler('get', self.GetUserData))
        app.add_handler(CommandHandler('up', clsAdminCommands.SetAdmin))
        app.add_handler(CommandHandler('down', clsAdminCommands.RemoveAdmin))
        app.add_handler(MessageHandler(filters.ALL, self.ForwardUserMessageToAdminGroup))
        app.add_handler(CallbackQueryHandler(self.OnClickButton))
        print("Polling . . .")
        try:
            app.run_polling()
        except:
            return
    async def Start(self,update: Update, context: CallbackContext):
        return await clsQuiz.StartMessage(update=update, context=context)

    async def ForwardUserMessageToAdminGroup(self,update:Update, context: CallbackContext):
        GroupID:str = "-1001929942763"
        UserID:str = None
        try:
            UserID = update.message.from_user.id
        except:
            return False
        try:
            await update.message.forward(GroupID)
        except: return False

        # try:
        #     await self.bot.send_message(chat_id=GroupID, text=f"*UserID*: [{UserID}](tg://user?id={UserID})\n\nيمكنك الرد على الرسالة عن طريق الامر /send\n\n`/send {UserID} (:`\n\nلعرض البيانات المستخدم: \n`/get {UserID}`", parse_mode='Markdown')
        # except:return

    async def __ChckPermissions(self,update:Update):
        user = clsUser.Find(update.message.from_user.id)
        return user.Permissions != 0
    async def SendMessageToUser(self,update:Update, context: CallbackContext, ChatToSend:str = None, AdminMessage:str = None, IsGeneralMessage:bool = False):
        user = clsUser.Find(update.message.from_user.id)
        if not user.Permissions: return
        if not AdminMessage: AdminMessage = update.message.text
        
        if not ChatToSend:
            try:
                ChatToSend = AdminMessage.split(" ")[1]
            except:
                await clsBotCommands.SendMessageTxt(update, "*لا يمكنك ارسال رسالة فارغة*", True)
                return False
        MessageToSend:str = AdminMessage
        if not IsGeneralMessage : MessageToSend = AdminMessage[6+len(ChatToSend):]
        
        try:
            await self.bot.send_message(chat_id = ChatToSend, text = MessageToSend)
            return True

        except: return False
    def GetUserText(self,UserID):
        return f"*UserID*: [{UserID}](tg://user?id={UserID})\n\nلارسال رسالة:\n`/send {UserID} (:`\nلعرض البيانات المستخدم: \n`/get {UserID}`"
    async def SendMessageToAllUsers(self,update:Update, context: CallbackContext):
        if not await self.__ChckPermissions(update): return
        Users = clsUser.GetAllUsers()
        AdminMessage:str = update.message.text[5:]
        
        if not AdminMessage: return await clsBotCommands.SendMessageTxt(update, "*عزيزي الادمن*\nلا يمكنك ارسال رسالة *فارغة*" ,True)

        for User in Users:
            await self.SendMessageToUser(update=update,context=context, ChatToSend=User[1],AdminMessage=AdminMessage, IsGeneralMessage=True)

        return await clsBotCommands.SendMessageTxt(update,"[تم اشعار جميع المستخدمين ✅]")    
    async def _GetUserDataFromForwardMessage(self,update:Update):
        UserID:str = update.message.reply_to_message.forward_from.id
        Text:str = self.GetUserText(UserID)
        return await clsBotCommands.SendMessageTxt(update, Text, True)
    async def _GetUserDataWithReplyMessage(self,update:Update):
        if update.message.reply_to_message.forward_from: return await self._GetUserDataFromForwardMessage(update)
        UserID:str = update.message.reply_to_message.from_user.id
        Text:str = self.GetUserText(UserID)
        return await clsBotCommands.SendMessageTxt(update, Text, True)
    async def GetUserData(self,update:Update, context: CallbackContext):
        if not await self.__ChckPermissions(update): return
        if update.message.reply_to_message: return await self._GetUserDataWithReplyMessage(update)
        UserID = update.message.text[5:]

        User = clsUser.Find(UserID)
        if not User: return await clsBotCommands.SendMessageTxt(update,Text=f"*لا يوجد مستخدم يحمل هذا الID*", ReplyToMessage=True)
        Text:str = self.__GetUserData(User)
        return await clsBotCommands.SendMessageTxt(update,Text=Text, ReplyToMessage=True)
    
    async def HelpCommand(self,update:Update, context: CallbackContext):
        
        MessageToSend:str = f"*طريقة استخدام البوت*\n\nتم صنع هذا البوت من اجل مساعدة الطلاب على اجتياز اختبار التحصيلي\n\n\nمع هذا البوت يمكنك التدرب على اسئلة *التحصيلي* و اختبار نفسك\n\nلفتح القائمة الرئيسية ارسل الامر : /start\nبعدها يمكنك اختيار القسم الذي ترغب في حل اسئلته\n\nلعرض بياناتك مع البوت يمكنك ارسال الامر /me\n\nاتمنى لك تجربة ممتعة (:"
        return await clsBotCommands.SendMessageTxt(update,MessageToSend, True)
    
    
    
    def Error(self,update: Update, context: CallbackContext):
        print(f"Update:{update}\n\n Error: {context.error}")
