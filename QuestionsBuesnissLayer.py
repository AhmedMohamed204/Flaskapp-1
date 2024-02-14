from enum import Enum
from QuestionsDataAccessLayer import QuestionsDataAccessLayer




class clsQuestion:
        
    def __init__(self ,ID ,QuestionLink, QuestionLevel, RightAnswer, ExplainLink, Subject) -> None:
        self.ID = ID
        self.QuestionLink = QuestionLink
        self.QuestionLevel = QuestionLevel
        self.RightAnswer = RightAnswer
        self.ExplainLink = ExplainLink
        self.Subject = Subject
    
    @property
    def Get_ID(self):
        return self.ID
    
    @property
    def Get_QuestionLink(self):
        return self.QuestionLink
    def Set_QuestionLink(self, QuestionLink):
        self.QuestionLink = QuestionLink

    def Set_QuestionLevel(self,QuestionLevel):
        self.QuestionLevel = QuestionLevel
    @property
    def Get_QuestionLevel(self):
        return self.QuestionLevel
    
    def Set_RightAnswer(self, RightAnswer):
        self.RightAnswer = RightAnswer
    @property
    def Get_RightAnswer(self):
        return self.RightAnswer
    
    @property
    def Get_ExplainLink(self):
        return self.ExplainLink
    def Set_ExplainLink(self, ExplainLink):
        self.ExplainLink = ExplainLink
        
    @property
    def Get_Subject(self):
        return self.Subject
    def Set_Subject(self, Subject):
        self.Subject = Subject

    @staticmethod
    def Find(QuestionID:str):
        QuestionData = QuestionsDataAccessLayer.GetQuestion(QuestionID=QuestionID)
        if not QuestionData : return None
        return clsQuestion(QuestionData["ID"], QuestionData["QuestionLink"], QuestionData["QuestionLevel"], QuestionData["RightAnswer"], QuestionData["ExplainLink"], QuestionData["QuestionSubject"])
    
    @staticmethod
    def AddNewQuestion(QuestionLink: str, QuestionLvl:int, RightAnswer:str, ExplainLink:str, Subject:int):
        return QuestionsDataAccessLayer.AddQuestion(QuestionLink, QuestionLvl, RightAnswer, ExplainLink, Subject)
    
    def Save(self):
        return QuestionsDataAccessLayer.UpdateQuestion(self.ID, self.QuestionLink, self.QuestionLevel, self.RightAnswer, self.ExplainLink,self.Subject)
    

    @staticmethod
    def GetRandomQuestion(QuestionSubject:int):
        return QuestionsDataAccessLayer.GetRandomQuestion(QuestionSubject)
    @staticmethod
    def GetRandomQuestionFromRandomSubject():
        return QuestionsDataAccessLayer.GetRandomQuestionFromRandomSubject()
    @staticmethod
    def DeleteQuestion(QuestionID: str):
        return QuestionsDataAccessLayer.DeleteQuestion(QuestionID)
    
    @staticmethod
    def GetAllQuestions():
        return QuestionsDataAccessLayer.GetAllQuestions()
    
    @staticmethod
    def TotalQuestions():
        return QuestionsDataAccessLayer.QuestionsCount()
    

    @staticmethod
    def GetLastQuestion():
        return QuestionsDataAccessLayer.GetLastQuestionID()

