from enum import Enum
from pickle import FALSE
from UsersDataAccessLayer import UsersDataAccessLayer




class clsUser:
        
    
    def __init__(self ,ID ,UserID, TotalAnswers, TotalRightAnswers, Permissions) -> None:
        self.ID = ID
        self.UserID = UserID
        self.TotalAnswers = TotalAnswers
        self.TotalRightAnswers = TotalRightAnswers
        self.Permissions = Permissions
    
    @property
    def Get_ID(self):
        return self.ID
    @property
    def Get_UserID(self):
        return self.UserID

    def Set_TotalAnswers(self,TotalAnswers):
        self.TotalAnswers = TotalAnswers
    @property
    def Get_TotalAnswers(self):
        return self.TotalAnswers
    
    def Set_TotalRightAnswers(self, TotalRightAnswers):
        self.TotalRightAnswers = TotalRightAnswers
    @property
    def Get_TotalRightAnswers(self):
        return self.TotalRightAnswers
    
    @property
    def Get_Permissions(self):
        return self.Permissions
    def Set_Permissions(self, Permissions):
        self.Permissions = Permissions








    @staticmethod
    def Find(UserID:str):
        UsersDataAccessLayer.AddUser(UserID)
        UserData = UsersDataAccessLayer.GetUser(UserID=UserID)
        if not UserData : return None
        return clsUser(UserData["ID"], UserData["UserID"], UserData["TotalAnswers"], UserData["TotalRightAnswers"], UserData["Permissions"])
    
    @staticmethod
    def AddNewUser(UserID):
        return UsersDataAccessLayer.AddUser(UserID)
    
    def Save(self):
        return UsersDataAccessLayer.UpdateUser(self.UserID, self.TotalAnswers, self.TotalRightAnswers, self.Permissions)
    
    @staticmethod
    def DeleteUser(UserID: str):
        return UsersDataAccessLayer.DeleteUser(UserID)
    
    @staticmethod
    def GetAllUsers():
        return UsersDataAccessLayer.GetAllUsers()
    
    @staticmethod
    def TotalUsers():
        return UsersDataAccessLayer.UsersCount()
    
    @staticmethod
    def IsExist(UserID:str)->bool:
        return UsersDataAccessLayer.IsUserExist(UserID)