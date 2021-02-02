from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from Database import Database
import urllib.request
import schedule
import os 
from api.main import *


 




class Callback :
    @staticmethod
    def onRegisterd(name,pn):
        print("registerd")
    @staticmethod
    def onUnregisterd(pn):
        print("Unregistred")
    @staticmethod
    def onAtricleAdded(title,discription,imgpath):
        print("ON ARTICLE ADDED \n")
        imgpathR = '/programming/projects/Python/whatAppBot/'
        send_Atrticle(title,discription,imgpath)
  


db =  Database('l',Callback)


def insertDatabaseAndSend(driver,data):
    count = len(data)
    print("+++++++++",data,"++++++\n")
    for i in range(count):
        newsBox = WebDriverWait(driver,1).until(lambda d: d.find_elements_by_class_name('td-block-span6'))
        print("______________________",newsBox[i].text,"ATTEMPING _____________________________")
        newsBox[i].click()
        title = driver.find_element_by_class_name('entry-title').text
        discriptions = driver.find_elements_by_css_selector(".td-post-content p")
        image = driver.find_element_by_class_name('entry-thumb').get_attribute('src')
        vitualSpace   = list()
        for dis in discriptions:
            vitualSpace.append('\n'+dis.text)
        print(len(discriptions))
        discription = ''.join(vitualSpace)
        imgpath =  imgdown(image)
        print('*******',imgpath,"********")
        time.sleep(3)
        db.insertItem(title,discription,image,imgpath)
        print(title+"\n",discription+'\n',image)

        driver.back()
        time.sleep(3600)


option = Options()
option.headless = True
option.add_argument('-headless')
option.page_load_strategy = 'none'

def fetch_data():
    try:
        with webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',options=option) as driver:
            print("BEFORE WAIT")
            wait = WebDriverWait(driver, 10)
            print("AFTER WAIT")
            driver.get("http://techguru.lk/")
            print("LODED")
            newsBox =  driver.find_elements_by_class_name('td-block-span6')
            insertDatabaseAndSend(driver,newsBox)
            print("Closing Driver")
            driver.close()
    except Exception as e:
        print("Erro At fetch_data - ", e)



def imgdown(url):
    print("Downloading")
    r = urllib.request.urlopen(url)
    name ='./images/'+ url.rsplit('/')[-1].rsplit("?")[0]
    if(os.path.isdir('./images') != True):
        os.mkdir('./images')

    print(name)
    with open(name, "wb+") as f:
        f.write(r.read())
        return os.path.abspath(f.name)

def send_Atrticle_fromDB():
    try:
        data =  db.getRandomItems()
        send_Atrticle(data[2],data[3],data[5])
    except Exception as e:
        print("Erro @ send_atricle_from db - ",e)
fetch_data()

#main Code 

schedule.every(2).hours.do(fetch_data)
schedule.every(8).hours.do(send_Atrticle_fromDB)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
    
