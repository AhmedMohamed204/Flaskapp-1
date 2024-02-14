import telegram
from QuestionsBuesnissLayer import clsQuestion
from UsersBusinessLayer import clsUser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CallbackQueryHandler, Updater, CommandHandler, MessageHandler, CallbackContext
from clsBotCommands import clsBotCommands

class clsQuiz(clsQuestion):

    MainMessage = {
            "Text":"*◄اهلا بك في بوت كويز التحصيلي*\nيمكنك اختيار القسم الذي ترغب في حل اسئلته عن طريق النقر على احد الازرار ادناه",
            "Buttons": [
                [InlineKeyboardButton("رياضيات", callback_data='رياضيات'),InlineKeyboardButton("فيزياء", callback_data='فيزياء') ],
                [InlineKeyboardButton("أحياء", callback_data='احياء'), InlineKeyboardButton("كيمياء", callback_data='كيمياء')],
                [InlineKeyboardButton("عشوائي", callback_data='عشوائي')]
                        ]
        }
    def QuestionButtons():
        Buttons = [
                [InlineKeyboardButton("ب", callback_data='ب'),InlineKeyboardButton("ا", callback_data='ا') ],
                [InlineKeyboardButton("د", callback_data='د'), InlineKeyboardButton("ج", callback_data='ج')]
                        ]
        return Buttons
    

    def NextQuestionButtons(Subject):
        Buttons = [
                [InlineKeyboardButton("الصفحة الرئيسية", callback_data='Main')]
                ,[InlineKeyboardButton("السؤال التالي", callback_data=f"{Subject}") ]
                        ]
        return Buttons

    async def StartMessage(update: Update, context: CallbackContext, ReplyToMessage = True):
        await clsBotCommands.SendPhoto( update=update,Photo="https://t.me/hfhdjdjsaksklsldkfkfkksoalcckxfr/21", Caption=clsQuiz.MainMessage["Text"], ReplyToMessage=ReplyToMessage, ButtonsList=clsQuiz.MainMessage["Buttons"])

    async def ChangeQuestionSubjectFromNumberToLetter(QuestionSubject:int):
        if QuestionSubject == 1: return "رياضيات"
        if QuestionSubject == 2: return "فيزياء"
        if QuestionSubject == 3: return "كيمياء"
        return "احياء"
       
    async def ChangeQuestionSubjectFromLetterToNumber(QuestionSubject:str):
        if QuestionSubject == "رياضيات":return 1
        if QuestionSubject == "فيزياء": return 2
        if QuestionSubject == "كيمياء": return 3
        return 4
       

    async def ChangeQuestionLevelFromNumberToLetter(QuestionLevel:int):
        if QuestionLevel == 1: return "سهل"
        if QuestionLevel == 2: return "متوسط"
        return "صعب"
      
    async def ChangeQuestionLevelFromLetterToNumber(QuestionLevel:str):
        if QuestionLevel == "سهل" : return 1
        if QuestionLevel =="متوسط": return 2
        return 3
    async def SendQuestionByLink(update: Update, QuestionLink:str, Text:str):
        return await clsBotCommands.SendPhoto(update=update, Photo=QuestionLink,ReplyToMessage=True, Caption=Text)
    async def SendQuestion(Subject,update: Update, context: CallbackContext):
        try:
            await update.callback_query.answer()
        except:
            return
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        QuestionDetails = None
        Suffix:str = ""
        if Subject == -1 :
            QuestionDetails= clsQuiz.GetRandomQuestionFromRandomSubject()
            Suffix+= "\n*عشوائي*"
        else:
            QuestionDetails= clsQuiz.GetRandomQuestion(Subject)
        QuestionSubject:str = await clsQuiz.ChangeQuestionSubjectFromNumberToLetter(QuestionSubject=QuestionDetails["QuestionSubject"])
        QuestionLevel:str = await clsQuiz.ChangeQuestionLevelFromNumberToLetter(QuestionLevel=QuestionDetails["QuestionLevel"])
        QuestionLink:str = QuestionDetails["QuestionLink"]
        Caption:str = f"*ID: {QuestionDetails['ID']}*\n*المادة: ~{QuestionSubject}~*\n*مستوى الصعوبة: {QuestionLevel}*" + Suffix
        return await clsBotCommands.SendPhoto(update=update.callback_query,Photo=QuestionLink, Caption=Caption, ButtonsList=clsQuiz.QuestionButtons())        
    
    def _IsRightAnswer(Answer:str, QuestionRightAnswer):
        return Answer == QuestionRightAnswer
    
    async def PerformUserAnswer(update: Update, context: CallbackContext):
        try:
            await update.callback_query.answer()
        except:
            return
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        
        CaptionOfMessage:str = update.callback_query.message.caption
        QuestionID = CaptionOfMessage.split("\n")[0][4:]
        Question = clsQuiz.Find(QuestionID)
        User = clsUser.Find(update.callback_query.message.chat.id)
        User.TotalAnswers += 1 
        
        RightAnswer = Question.RightAnswer
        UserAnswer:str = update.callback_query.data
        caption:str = ""
        if not clsQuiz._IsRightAnswer(UserAnswer, RightAnswer): caption = "*❌ اجابة خاطئة ❌*"
        else : 
            caption = "*اجابة صحيحة ✅*"
            User.TotalRightAnswers += 1
        User.Save()
            
        caption += f"\nالاجابة الصحيحة: {RightAnswer}"
        Subject = None
        if "عشوائي" in CaptionOfMessage: 
            Subject = "عشوائي"
        else:
             Subject = await clsQuiz.ChangeQuestionSubjectFromNumberToLetter(Question.Subject)
        await clsBotCommands.SendPhoto(update.callback_query, Photo=Question.ExplainLink, Caption=caption, ButtonsList=clsQuiz.NextQuestionButtons(Subject))
    
    async def Main(update: Update, context: CallbackContext):
        try:
            await update.callback_query.answer()
        except:
            return
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await clsQuiz.StartMessage(update=update.callback_query,context= context, ReplyToMessage=False)




