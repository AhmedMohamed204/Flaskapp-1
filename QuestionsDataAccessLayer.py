import sqlite3

class QuestionsDataAccessLayer:

    def AddQuestion(QuestionLink: str, QuestionLvl:int, RightAnswer:str, ExplainLink:str, Subject:int):
        IsAdded: bool = False;
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        query:str = f"INSERT OR IGNORE INTO Questions(QuestionURL, QuestionLevl, RightAnswer, ExplainURL, QuestionSubject) values (\"{QuestionLink}\",{QuestionLvl},\"{RightAnswer}\",\"{ExplainLink}\",{Subject});"
        cr.execute(query)
        db.commit()
        IsAdded = (db.total_changes > 0)
        db.close()
        return IsAdded

    def DeleteQuestion(QuestionID: str):
        IsDeleted: bool = False;
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute(f"Delete FROM Questions WHERE Questions.ID = {QuestionID};")
        db.commit()
        IsDeleted = (db.total_changes > 0)
        db.close()
        return IsDeleted
    
    def UpdateQuestion(QuestionID:str ,QuestionLink: str, QuestionLevl:int, RightAnswer:str, ExplainLink:str, Subject:int) -> bool:
        query:str = f"Update Questions set QuestionURL=\"{QuestionLink}\", QuestionLevl={QuestionLevl}, RightAnswer=\"{RightAnswer}\", ExplainURL=\"{ExplainLink}\" , QuestionSubject={Subject} WHERE ID = {QuestionID};"
        IsUpdated: bool = False;
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute(query)
        db.commit()
        IsUpdated = (db.total_changes > 0)
        db.close()
        return IsUpdated
    
    def GetQuestion(QuestionID : str):
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        query:str = f"SELECT * FROM Questions WHERE ID = {QuestionID}"
        try:
            cr.execute(query)
        except:
            return
        QuestionDetails = cr.fetchone()
        if not QuestionDetails: return None
        ID = QuestionDetails[0]
        QuestionLink = QuestionDetails[1]
        QuestionLevel = QuestionDetails[2]
        RightAnswer = QuestionDetails[3]
        ExplainLink = QuestionDetails[4]
        QuestionSubject = QuestionDetails[5]
        db.commit()
        QuestionDectionary = {
                "ID": ID,
                "QuestionLink": QuestionLink,
                "QuestionLevel": QuestionLevel,
                "RightAnswer": RightAnswer,
                "ExplainLink": ExplainLink,
                "QuestionSubject": QuestionSubject
            }
        db.close()
        return QuestionDectionary

    def GetRandomQuestion(QuestionSubject:int):
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        query:str = f"select * from Questions Where QuestionSubject = {QuestionSubject} order by random() limit 1"
        cr.execute(query)
        QuestionDetails = cr.fetchone()
        if not QuestionDetails: return None
        ID = QuestionDetails[0]
        QuestionLink = QuestionDetails[1]
        QuestionLevel = QuestionDetails[2]
        RightAnswer = QuestionDetails[3]
        ExplainLink = QuestionDetails[4]
        QuestionSubject = QuestionDetails[5]
        db.commit()
        QuestionDectionary = {
                "ID": ID,
                "QuestionLink": QuestionLink,
                "QuestionLevel": QuestionLevel,
                "RightAnswer": RightAnswer,
                "ExplainLink": ExplainLink,
                "QuestionSubject": QuestionSubject
            }
        db.close()
        return QuestionDectionary
    
    def GetRandomQuestionFromRandomSubject():
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        query:str = f"select * from Questions   order by random() limit 1"
        cr.execute(query)
        QuestionDetails = cr.fetchone()
        if not QuestionDetails: return None
        ID = QuestionDetails[0]
        QuestionLink = QuestionDetails[1]
        QuestionLevel = QuestionDetails[2]
        RightAnswer = QuestionDetails[3]
        ExplainLink = QuestionDetails[4]
        QuestionSubject = QuestionDetails[5]
        db.commit()
        QuestionDectionary = {
                "ID": ID,
                "QuestionLink": QuestionLink,
                "QuestionLevel": QuestionLevel,
                "RightAnswer": RightAnswer,
                "ExplainLink": ExplainLink,
                "QuestionSubject": QuestionSubject
            }
        db.close()
        return QuestionDectionary

    def GetAllQuestions():
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute("SELECT * FROM Questions")
        Questions:str = cr.fetchall()        
        db.commit()
        db.close()
        return Questions

    def QuestionsCount():
        query:str = "select count(id) from Questions"
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute(query)
        QuestionsCount = cr.fetchone()
        db.commit()
        db.close()
        return QuestionsCount[0]
    
    def GetLastQuestionID():
        query:str = "select ID from Questions ORDER By ID desc limit 1"
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute(query)
        QuestionDetails = cr.fetchone()
        db.commit()
        db.close()
        return QuestionDetails[0]
        