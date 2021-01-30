from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
import time

no_of_message = 1  # n of o.time you want the message to be send
moblie_no_list = ['🏏🎾New zeland cricket🎾🏏']  # list of phone number can be of any length


def element_presence(driver,by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)





def send_Whatsapp_image(driver,path,fDiscription=""):
    print("FILE SENDING")
    element_presence(driver,
        By.XPATH, "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[1]/div[2]/div/div", 20)
    driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[1]/div[2]/div/div").click()
    print("CLICK ELEMENT")
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input").send_keys(path)
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]').send_keys(
    fDiscription
    )
    time.sleep(3)
    driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div").click()
    time.sleep(20)
    print("Img Sended")


def send_whatsapp_msg(driver,name,title,text,imgpath):
    sleep(10)
    user = findUser(driver, name)
    print("USER", user)
    # user = driver.find_element_by_xpath("//span[@title='{}']".format(name))
    if(user != None):
        user.click()
        send_Whatsapp_image(driver,imgpath, title)
    else:
        raise ElementNotInteractableException("element Not get")
    element_presence(driver,
        By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]', 50)
    txt_box = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
    global no_of_message
    for x in range(no_of_message):
        txt_box.send_keys(text)
        time.sleep(2)
        txt_box.send_keys("\n")


def formatDiscription(title, discription):
    after = f'       *{title}*           {discription}'
    return after


def findUser(driver, name):
    print("Find USer")
    el = None
    try:
        el = driver.find_element_by_xpath("//span[@title='{}']".format(name))
    except:
        print("SERACHIGN")
        element_presence(driver,By.XPATH,'/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]',50)
        search = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')
        time.sleep(10)
        print(search)
        search.click()
        time.sleep(5)
        search.send_keys(name)
        time.sleep(7)
        print("AFTER 7 MINITE")
        try:
            wait = WebDriverWait(driver, 5, poll_frequency=1, ignored_exceptions=[
                                 ElementNotVisibleException, ElementNotSelectableException])
            wait.until(lambda d: d.find_element_by_css_selector(
                "span.matched-text"))
            el = driver.find_element_by_css_selector("span.matched-text")
            print(el)
        except Exception as e:
            print("invailid phone no :"+str(name), e)
    print(el)
    return el

option = Options()
option.headless = True
option.page_load_strategy = 'none'

def send_Atrticle(title,discription,imgpath):
    # driver = webdriver.Chrome(executable_path="chromedriver.exe")
    profile = webdriver.FirefoxProfile(
        '/home/anuradhedilshan/.mozilla/firefox/iuw0usk9.Default User')
    driver = webdriver.Firefox(
        profile, executable_path='/programming/projects/Python/whatAppBot/geckodriver',options=option)
    driver.get("http://web.whatsapp.com")
    sleep(10)  # wait time to scan the code in second
    print("Send ARTICLE")
    text  = formatDiscription(title,discription)
    for moblie_no in moblie_no_list:
        try:
            send_whatsapp_msg(driver,moblie_no,title,text,imgpath)
            time.sleep(10)
        except Exception as e:
            print("error", e)
            sleep(10)
            
    driver.close()

print('Api/main SCRIPT Ended')