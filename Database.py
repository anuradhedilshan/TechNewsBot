import sqlite3
from sqlite3 import Error
import datetime
import random

class Database:
    Callback = None
    cursorObj = None
    con = None
    
    def __init__(self, databasePath,Callback):
        
        self.connect('db.db')
        self.Callback = Callback
        

    def connect(self, execpath):
        try:
            self.con = sqlite3.connect(execpath)
            self.cursorObj = self.con.cursor()
            print("SD")
            self.createTable()
            

        except Error as e:
            print(e, "@ database.py Line - 6 ")
            exit()

    def createTable(self):
        if(self.cursorObj != None):
            self.cursorObj.execute("CREATE TABLE IF NOT EXISTS articles(" +
              "ID integer PRIMARY KEY," +
              "date datetime ," +
              "title varchar(200) not null ," +
              "discription longtext not null ," +
              "image varchar(500) not null ," +
              "imagepath varchar(70) not null,"+
              "media varchar(500) ," +
              "morelink varchar(500) " +
             ")")

            self.cursorObj.execute(
              "CREATE TABLE IF NOT EXISTS register(" +
              "id integer," +
              "date datetime ," +
              "name varchar(200) not null ," +
              "pnumber varchar(15) not null ," +
              "PRIMARY KEY (id) ,  UNIQUE (pnumber) )")

            self.con.commit()

        else:
            raise Error("CAnt Create Table @database.py line 29")


    def insertItem(self, title, dis, img,imgpath, media = '', more = ''):
        if(self.cursorObj.execute(f"SELECT  COUNT(*) FROM articles WHERE title = '{title}'").fetchone()[0] < 1):

            time=(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            print(time)
            self.cursorObj.execute(
                f"INSERT INTO articles (date,title,discription,image,imagepath,media,morelink) VALUES('{time}','{title}','{dis}','{img}','{imgpath}','{media}','{more}')"
            )
            self.con.commit()
            self.Callback.onAtricleAdded(title,dis,imgpath)
        else:
            
            print("ALERDY ADDED")

    def registerUser (self, name, pnumber):
        if(self.cursorObj.execute(f"SELECT  COUNT(*) FROM articles WHERE pnumber = {pnumber}").fetchone()[0] < 1): 
            time=(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            print(time)
            self.cursorObj.execute(
            f"INSERT INTO articles (date,name,pnumber) VALUES('{time}','{name}','{pnumber}')"
            )
            self.con.commit()
            self.Callback.onRegisterd(name,pnumber)
        else:
            self.Callback.onRegisterd(name,pnumber)

    def unregisterUser (self, pnumber):
        time=(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        print(time)
        self.cursorObj.execute(
            f"DELETE FROM register WHERE pnumber = {pnumber}"
        )
        self.con.commit()
        self.Callback.onUnregisterd(pnumber)

    def getRandomItems(self):
        count = 0
        if(self.cursorObj != None):
            count = int(self.cursorObj.execute("SELECT  COUNT(*) FROM articles").fetchone()[0])
            print(count)
            randomIndex = random.randrange(0, count, 1)
            data =  self.cursorObj.execute(f"SELECT * FROM articles WHERE ID = {randomIndex} LIMIT 1 ").fetchone()
            return data
            #truple

            







