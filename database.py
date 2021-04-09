import pycurl
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
    def sentCount(self):
        with conn:
            c.execute("SELECT * FROM Users WHERE send = 2")
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
            c.execute("DELETE FROM users WHERE NOT send = 0")

class Proxy:
    @classmethod
    def add(self, address):
        if address.split('.')[-1] == "txt":
            with open(address) as f:
                for proxy in f.read().split("\n"):
                    with conn:
                        c.execute("INSERT INTO 'main'.'Proxies'('id','address','used') VALUES (NULL,?,0)",(proxy,))
                    print("Added: "+proxy)
        else:
            with conn:
                c.execute(f"INSERT INTO 'main'.'Proxies'('id','address','used') VALUES (NULL,?,0)",(address,))
            print("Added\n")
    
    @classmethod
    def get(self, sec = False):
        if not sec:
            print("Checking proxies...")
        with conn:
            c.execute("SELECT * FROM Proxies")
            proxies = c.fetchall()

        # return proxy
        for proxy in proxies:
            if not proxy[2]:
                if not self.check(proxy[1]):
                    print("Proxy: "+proxy[1]+" Failed, removing...")
                    with conn:
                        c.execute(f"DELETE FROM Proxies WHERE id = {proxy[0]}")
                        c.execute("SELECT * FROM Proxies")
                        proxies = c.fetchall()
                else:
                    with conn:
                        c.execute(f"UPDATE Proxies SET used = 1 WHERE id = {proxy[0]}")
                    print("Proxy: "+proxy[1])
                    return proxy[1]

        # check available proxies
        count = len([proxy for proxy in proxies if not proxy[2]])
        if not count and not sec:
            with conn:
                c.execute(f"UPDATE Proxies SET used = 0")
            return self.get(True)
        elif not count and sec: 
            print("No proxy")
            return False

    @classmethod        
    def check(self, addr):
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.URL, "https://example.com")
            c.setopt(pycurl.PROXY, addr)
            c.setopt(pycurl.NOBODY, 1)
            c.setopt(pycurl.CONNECTTIMEOUT, 1000)
            c.perform()
            if c.getinfo(pycurl.RESPONSE_CODE) == 200:
                return True
            return False
        except:
            return False

    @classmethod
    def count(self):
        with conn:
            c.execute("SELECT * FROM Proxies")
            return len(c.fetchall())