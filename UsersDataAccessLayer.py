import sqlite3

class UsersDataAccessLayer:

    def AddUser(UserID: str):
        IsAdded: bool = False
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        try:
            cr.execute(f"INSERT OR IGNORE INTO users (UserID, TotalAnswers, TotalRightAnswers, Permissions) VALUES ({UserID}, 0, 0, 0);")
        except: return
        db.commit()
        IsAdded = (db.total_changes > 0)
        db.close()
        return IsAdded

    def DeleteUser(UserID: str):
        IsDeleted: bool = False;
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute(f"DELETE FROM Users WHERE users.UserID = {UserID};")
        db.commit()
        IsDeleted = (db.total_changes > 0)
        db.close()
        return IsDeleted
    
    def UpdateUser(UserID:str, TotalAnswers: int, TotalRightAnswers: int, Permissions: int):
        query:str = f"UPDATE users SET TotalAnswers = {TotalAnswers}, TotalRightAnswers = {TotalRightAnswers} , Permissions = {Permissions} WHERE UserID = {UserID};"
        IsUpdated: bool = False;
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute(query)
        db.commit()
        IsUpdated = (db.total_changes > 0)
        db.close()
        return IsUpdated
    
    def GetUser(UserID : str):
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        query:str = f"SELECT * FROM Users WHERE Users.UserID = {UserID}"
        try:
            cr.execute(query)
        except:return
        UserDetails = cr.fetchone()
        if not UserDetails: return None
        ID = UserDetails[0]
        UserID = UserDetails[1]
        TotalAnswers = UserDetails[2]
        TotalRightAnswers = UserDetails[3]
        Permissions = UserDetails[4]
        db.commit()
        UserDectionary = {
                "ID": ID,
                "UserID": UserID,
                "TotalAnswers": TotalAnswers,
                "TotalRightAnswers": TotalRightAnswers,
                "Permissions": Permissions
            }
        db.close()
       
        return UserDectionary

    def GetAllUsers():
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute("SELECT * FROM Users")
        Users:str = cr.fetchall()        
        db.commit()
        db.close()
        return Users
    
    def UsersCount():
        query:str = "select count(id) from users"
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute(query)
        UsersCount = cr.fetchone()
        db.commit()
        db.close()
        return UsersCount[0]
    
    def IsUserExist(UserID:str)->bool:
        IsExist:bool = False
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute(f"SELECT * FROM Users WHERE UserID = {UserID}")
        IsExist = (cr.fetchone() != None)       
        db.commit()
        db.close()
        return IsExist


