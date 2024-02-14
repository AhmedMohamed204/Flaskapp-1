from QuestionsBuesnissLayer import clsQuestion
from UsersBusinessLayer import clsUser
from telegram import  Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.ext import filters,Application, CallbackQueryHandler, Updater, CommandHandler, MessageHandler, CallbackContext
from clsBotCommands import clsBotCommands
from clsQuiz import clsQuiz

class clsAdminCommands:
    async def Dashboard(update: Update, context: CallbackContext):
        user = clsUser.Find(update.message.from_user.id)
        if not user.Permissions: return
        
        Message:str = f"اهلا بك *{update.message.from_user.first_name}* في لوحة التحكم.\n\n*عدد المستخدمين: {clsUser.TotalUsers()}*\n*عدد الاسئلة: {clsQuiz.TotalQuestions()}*\n\nيمكنك عرض بيانات اي سؤال عن طريق الامر `/show [id السؤال]`\n\nلاضافة سؤال: `/add` \nلحذف سؤال: `/delete [id]`\nللتعديل على سؤال: `/update`\n\nلعرض بيانات احد المستخدمين: `/get [UserID]`"
        return await clsBotCommands.SendMessageTxt(update=update, Text=Message, ReplyToMessage=True)
    
    async def __CheckQuestionData(update:Update, RightAnswer:str, Subject:str,QuestionLevel:str) ->bool:
        if RightAnswer not in ["ا", "ب", "ج", "د"]: return await clsBotCommands.SendMessageTxt(update=update,Text="الاجابة الصحيحة يبجب ان تكون ا او ب او ج او د\n\nتأكد من ان \'ا\' بدون همزة", ReplyToMessage=True)
        if Subject not in ["رياضيات", "فيزياء", "كيمياء", "احياء"]: return await clsBotCommands.SendMessageTxt(update=update,Text="المادة يجب ان تكون\n\n\'رياضيات\'\n\'فيزياء\'\n\'كيمياء\'\n\'احياء (بدون همزة)\'", ReplyToMessage=True)
        if QuestionLevel not in ["سهل", "متوسط", "صعب"]: return await clsBotCommands.SendMessageTxt(update=update,Text="الصعوبة يجب ان تكون\n\n\'سهل\'\n\'متوسط\'\n\'صعب\'\n", ReplyToMessage=True)
        return True
    
    async def __CheckMessageLength(update:Update ,UserMessageLength:str, Message:str, MaximumLength:int = 5):
        if UserMessageLength <= 1:
            await clsBotCommands.SendMessageTxt(update=update,Text=Message, ReplyToMessage=True)
            return False
        if UserMessageLength < MaximumLength: 
            await clsBotCommands.SendMessageTxt(update=update,Text="البيانات التي قمت بادخالها ناقصة\nتأكد من انك ادخلت جميع البيانات المطلوبة(:", ReplyToMessage=True)
            return False
        if UserMessageLength > MaximumLength: 
            await clsBotCommands.SendMessageTxt(update=update,Text="البيانات المدخلة زائدة", ReplyToMessage=True)
            return False
        
        return True

    async def __CheckQuestionLinks(update:Update, QuestionLink:str, Explain:str):
        if not await clsQuiz.SendQuestionByLink(update=update, QuestionLink=QuestionLink,Text=""):
            await clsBotCommands.SendMessageTxt(update=update, ReplyToMessage=True, Text="صورة السؤال غير صالحة.. اعد المحاولة مع رابط اخر") 
            return False
        if not await clsQuiz.SendQuestionByLink(update=update, QuestionLink=Explain,Text=""):
            await clsBotCommands.SendMessageTxt(update=update, ReplyToMessage=True, Text="صورة شرح السؤال غير صالحة.. اعد المحاولة مع رابط اخر") 
            return False
        return True
    async def AddQuestion(update: Update, context: CallbackContext):
        user = clsUser.Find(update.message.from_user.id)
        if not user.Permissions: return
        UserMessage:str = update.message.text
        UserMessageLength:int = len(UserMessage.split("\n"))
        Message:str = f"لاضافة سؤال جديد اتبع الخطوات التالية\n\n/add -رابط صورة السؤال-\n-رابط شرح السؤال او نفس رابط السؤال-\n-الاجابة الصحيحة-\n-المادة-\n-مستوى صعوبة السؤال-\n\n\n\nالمادة: [رياضيات,فيزياء,كيمياء,احياء]\nمستوى الصعوبة: [سهل,متوسط,صعب]"

        if not await clsAdminCommands.__CheckMessageLength(update=update, UserMessageLength=UserMessageLength, Message=Message): return

        UserMessage = UserMessage[5:].split("\n")
        QuestionLink:str = UserMessage[0]
        ExplainLink:str = UserMessage[1]
        RightAnswer:str = UserMessage[2]
        Subject:str = UserMessage[3]
        QuestionLevel:str = UserMessage[4]

        if await clsAdminCommands.__CheckQuestionData(update=update, RightAnswer=RightAnswer, QuestionLevel=QuestionLevel, Subject=Subject) != True: return 
        if ExplainLink == ".": ExplainLink = QuestionLink
        Subject = await clsQuiz.ChangeQuestionSubjectFromLetterToNumber(Subject)
        QuestionLevel = await clsQuiz.ChangeQuestionLevelFromLetterToNumber(QuestionLevel)
        if await clsAdminCommands.__CheckQuestionLinks(update=update, QuestionLink=QuestionLink, Explain=ExplainLink) != True:return

        clsQuestion.AddNewQuestion(QuestionLink=QuestionLink, QuestionLvl=QuestionLevel, RightAnswer=RightAnswer, ExplainLink=ExplainLink, Subject=Subject)
        
        question = clsQuestion.Find(clsQuestion.GetLastQuestion())
        
        return await clsAdminCommands.ShowQuestion(update,context, question.ID)
    
    async def SendChatID(update: Update, context: CallbackContext):
        return await clsBotCommands.SendMessageTxt(update=update, Text=update.message.chat.id, ReplyToMessage=True)
    
    async def __ShowQuestionCaption(Question:clsQuestion):
        Subject:str = await clsQuiz.ChangeQuestionSubjectFromNumberToLetter( Question.Subject)
        Level:str = await clsQuiz.ChangeQuestionLevelFromNumberToLetter( Question.QuestionLevel)
        return f"*ID*: {Question.ID}\n*Subject*: {Subject}\n*Right Answer*: {Question.RightAnswer}\n*Question Level*: {Level}"
    async def ShowQuestion(update: Update, context: CallbackContext, QuestionID:str = None):
        
        if not QuestionID: QuestionID = update.message.text[6:]
        Question = clsQuestion.Find(QuestionID)
        Button = [[InlineKeyboardButton("صورة شرح السؤال", callback_data='ShowExplain')]]

        if not Question: return await clsBotCommands.SendMessageTxt(update,"لم اتمكن من العثور على السؤال", True)
        return await clsBotCommands.SendPhoto(update,Question.QuestionLink, await clsAdminCommands.__ShowQuestionCaption(Question) ,False,Button)
    async def __EditShowMessage(update:Update, Explain:bool = False):
        try:
            await update.callback_query.answer()
        except:
            return
        QuestionID:str = update.callback_query.message.caption.split("\n")[0][4:]
        Question = clsQuestion.Find(QuestionID)
        if not Question: return
        Photo:str = Question.QuestionLink
        CallData:str = "ShowExplain"
        ButtonText:str = "صورة شرح السؤال"
        if Explain:
            Photo = Question.ExplainLink
            CallData = "ShowQuestion"
            ButtonText = "صورة السؤال"
        Button = [[InlineKeyboardButton(ButtonText, callback_data=CallData)]]
        try:
            await update.callback_query.message.edit_media(
            
                media=InputMediaPhoto(
                    media= Photo,
                    caption=  await clsAdminCommands.__ShowQuestionCaption(Question),
                    parse_mode='Markdown'
                
                ),
                reply_markup=InlineKeyboardMarkup(Button)       
            )
            return True
        except:
            return False
    async def ShowExplainOfQuestion(update:Update, context: CallbackContext):
        return await clsAdminCommands.__EditShowMessage(update, True)
    async def ShowQuestionAfterExpalin(update:Update, context: CallbackContext ):
        return await clsAdminCommands.__EditShowMessage(update)
    
    async def __IsQuestionFound(update:Update, Question:clsQuestion):
        if not Question:
            await clsBotCommands.SendMessageTxt(update,"لم اتمكن من العثور على السؤال", True)
            return False
        return True
    async def DeleteQuestion(update:Update, context: CallbackContext, QuestionID:str = None ):
        user = clsUser.Find(update.message.from_user.id)
        if not user.Permissions: return
        
        if not QuestionID: QuestionID = update.message.text[8:]
        
        Question = clsQuestion.Find(QuestionID)        
        if not await clsAdminCommands.__IsQuestionFound(update,Question): return False
        
        if  clsQuestion.DeleteQuestion(QuestionID): return await clsBotCommands.SendMessageTxt(update,f"تم حذف السؤال\n\nيمكنك التأكد عن طريق ارسال الامر التالي\n\n`/show {Question.ID}`", True)
        return await clsBotCommands.SendMessageTxt(update,"حدث خطأ تسبب في عدم اكمال اجراءات حذف السؤال\n\nاعد المحاولة مرة اخرى.", True)

    
    async def UpdateQuestion(update:Update, context: CallbackContext):
        user = clsUser.Find(update.message.from_user.id)
        if not user.Permissions: return
        UserMessage:str = update.message.text
        UserMessageLength:int = len(UserMessage.split("\n"))
        Message:str = f"للتعديل على سؤال اتبع الخطوات التالية\n\n/update -id السؤال-\n -رابط صورة السؤال-\n-رابط شرح السؤال او نفس رابط السؤال-\n-الاجابة الصحيحة-\n-المادة-\n-مستوى صعوبة السؤال-\n\n\n\nالمادة: [رياضيات,فيزياء,كيمياء,احياء]\nمستوى الصعوبة: [سهل,متوسط,صعب]\n\nاذا لم ترد تعديل احد عناصر السؤال, يمكنك كتابة \'.\' مكانه\nاذا كانت تريد جعل رابط الشرح هو رابط السؤال يمكنك كتابة \'..\' و نفس الشيء بالنسبة لرابط السؤال"
        
        if not await clsAdminCommands.__CheckMessageLength(update=update, UserMessageLength=UserMessageLength, Message=Message, MaximumLength=6): return
        UserMessage = UserMessage[8:].split("\n")
        QuestionID:str = UserMessage[0]
        QuestionLink:str = UserMessage[1]
        ExplainLink:str = UserMessage[2]
        RightAnswer:str = UserMessage[3]
        Subject:str = UserMessage[4]
        QuestionLevel:str = UserMessage[5]
        Question = clsQuestion.Find(QuestionID)
        print(QuestionID)
        if not await clsAdminCommands.__IsQuestionFound(update, Question): return
        
        if ExplainLink == ".": ExplainLink = Question.ExplainLink
        if ExplainLink == "..": ExplainLink = Question.QuestionLink
        if QuestionLink == ".": QuestionLink = Question.QuestionLink
        if QuestionLink == "..": QuestionLink = Question.ExplainLink
        if RightAnswer == ".": RightAnswer= Question.RightAnswer
        if Subject == ".": Subject= Question.Subject
        if QuestionLevel == ".": QuestionLevel = Question.QuestionLevel
    
        if await clsAdminCommands.__CheckQuestionData(update=update, RightAnswer=RightAnswer, QuestionLevel=QuestionLevel, Subject=Subject) != True: return 
        Subject = await clsQuiz.ChangeQuestionSubjectFromLetterToNumber(Subject)
        QuestionLevel = await clsQuiz.ChangeQuestionLevelFromLetterToNumber(QuestionLevel)
        
        if await clsAdminCommands.__CheckQuestionLinks(update=update, QuestionLink=QuestionLink, Explain=ExplainLink) != True:return
        
        
        Question.QuestionLink = QuestionLink
        Question.ExplainLink = ExplainLink
        Question.RightAnswer = RightAnswer
        Question.Subject = Subject
        Question.QuestionLevel = QuestionLevel
        Question.Save()
        return await clsAdminCommands.ShowQuestion(update,context,Question.ID )
     
    async def __EditUserPermessions(update:Update, context: CallbackContext, Permissions:int):
        MessageText = update.message.text
        MessageLen = len(MessageText.split(" "))
        if 1 >  MessageLen or MessageLen > 2: return;
        
        UserToBeAdmin:clsUser = None
        if not clsUser.IsExist( MessageText.split(" ")[1]): return await clsBotCommands.SendMessageTxt(update,"*لا يوجد مستخدم يحمل هذا الID*", True)
        try:
            UserToBeAdmin= clsUser.Find(MessageText.split(" ")[1])
        except: return False
        
        UserToBeAdmin.Permissions = Permissions
        
        UserToBeAdmin.Save()
        UserID:str = UserToBeAdmin.UserID
        text:str = f"*UserID*: [{UserID}](tg://user?id={UserID})\n*تمت العملية بنجاح*\n\n`/get {UserID}`"
        
        return await clsBotCommands.SendMessageTxt(update, text , True)
        
        

    
    async def SetAdmin(update:Update, context: CallbackContext):
        
        AdminUser:clsUser = clsUser.Find(update.message.from_user.id)
        if not AdminUser or not AdminUser.Permissions: return
        return await clsAdminCommands.__EditUserPermessions(update,context,-1)
    
    async def RemoveAdmin(update:Update, context: CallbackContext):
        
        AdminUser:clsUser = clsUser.Find(update.message.from_user.id)
        if AdminUser.Permissions != -2 or AdminUser.UserID != "2098036983": return
        return await clsAdminCommands.__EditUserPermessions(update,context,0)
    
