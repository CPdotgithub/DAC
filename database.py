import sqlite3

conn = sqlite3.connect('Data.db')
c = conn.cursor()

class DataBase:
    def __init__(self,username,uID,send):
        self.username = username
        self.uID = uID
        self.send = send
    
    @classmethod
    def GetFromDB(self):
        with conn:
            c.execute("SELECT * FROM Users")
            return c.fetchall()

    def GoToDB(self):
        with conn:
            c.execute(f"INSERT INTO 'main'.'Users'('ID','username','uID','send') VALUES (NULL,?,'{self.uID}',{self.send})",(self.username,))


    @classmethod
    def SendUpdate(self,uID):
        value = 1
        with conn:
            c.execute(f"UPDATE Users SET send = {value} WHERE uID = {uID}")
    
    @classmethod
    def Status(self,uID):
        with conn:
            c.execute(f'SELECT uID FROM Users WHERE uID = "{uID}"')
            if len(c.fetchall()) == 0:
                return False
            else:
                return True
    
    @classmethod
    def Count(self):
        with conn:
            c.execute("SELECT * FROM Users")
            return len(c.fetchall())

    @classmethod
    def nCount(self):
        with conn:
            c.execute("SELECT * FROM Users WHERE send = 1")
            return len(c.fetchall())

    @classmethod
    def Reset(self):
        value = 0
        with conn:
            c.execute(f"UPDATE Users SET send = {value}")
            print("Reset is Done!")

    @classmethod
    def truncate(self):
        with conn:
            c.execute("DELETE FROM users WHERE send = 1")