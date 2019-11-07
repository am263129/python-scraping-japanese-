from lxml import html
import requests
import codecs
import timeit
import time, threading
import queue,sys,subprocess
import pickle
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from requests_html import HTML
from threading import Thread
from selenium.webdriver.chrome.options import Options


def report_to_a(filename,data):
    with open("%s.txt"%filename,"a") as f:
        f.write(time.ctime())
        f.write("\n")
        f.write(data)
        f.write("\n")

def thread_cart():
    
    if q.empty():
        print("Empty Queue")    
    while not q.empty():
        value = q.get()
        print(value)
        print(value[0])
        url = value[0]
        index = value[1]
        driver = working_drivers[index]
        print("milestone_2")
        btn_add_cart = driver.find_element_by_xpath(".//form/span/input")
        btn_add_cart.click()
        print("milestone_3")
        err_msg = None
        try:
            err_msg = driver.find_element_by_xpath(".//div/section/p[@class = 'err']").get_attribute("innerHTML")
            print("Damn!", err_msg,len(err_msg))
        except:
            print("seems to be success")
        if err_msg == None:
            try:
                result = None
                result = driver.find_element_by_xpath(".//tbody/tr/td[@class = 'delete']")
                if result == None:
                    print("Unknown Error")
                else:
                    cookies = driver.get_cookies()
                    for cookie in cookies:
                        if cookie["name"]=="ZOZO%5FUID":
                            _cookie = cookie["value"]
                        if cookie["name"][0:10] == "ASPSESSION":
                            _cookie_session = cookie["value"]
                    print("ASPSESSION : ", _cookie_session, " ID : ", _cookie)
                    report_to_a("ONE_CART!","URL :" + url + ">>>" +"ZOZO%5FUID : " + _cookie + " ASPSESSION : " + _cookie_session)
            except:
                print("Failed")
                
        q.task_done()
def put_in_queue(urls, index):
    q.put([urls,index])

def multi_thread():
    t1 = Thread(target = thread_cart)
    print("Started one thread")
    t1.start()
def Create_Driver(url):
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    # options.add_argument('--disable-infobars')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--profile-directory=default')
    # options.add_argument('--incognito')
    # options.add_argument('--disable-plugin-discovery')
    # options.add_argument('--start-maximized')
    # driver = webdriver.Chrome(executable_path="/root/ragtag/chromedriver", chrome_options = options)
    prefs = {
	"profile.managed_default_content_settings.images":2,
	"--disable-bundled-ppapi-flash":1
	}
    options = Options()
    options.add_argument('--disable-logging')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", prefs)
    print("start_driver")
    driver = webdriver.Chrome("chromedriver.exe", chrome_options = options)
    print("started driver")
    driver.get(url)
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie["name"]=="ZOZO%5FUID":
            _cookie = cookie["value"]
        if cookie["name"][0:10] == "ASPSESSION":
            _cookie_session = cookie["value"]
    return driver


def Log_in():
    l_point1 = time.time()
    while True:
        try:
            driver = Create_Driver("https://zozo.jp/_member/login.html")
            time.sleep(3)
            print("try to login")
            username = driver.find_element_by_xpath(".//li[@id = 'memID']/input")
            userpassword = driver.find_element_by_xpath(".//li[@id = 'passWord']/input")
            print("getting input successful")
            username.send_keys("x0xenx@gmail.com")
            userpassword.send_keys("0771397840xe")
            btn_login = driver.find_element_by_xpath(".//div[@class = 'container clearfix']/p[@class = 'btn']/input")
            btn_login.click()
            break
        except:
            time.sleep(1)       
    l_point2 = time.time()
    print("time for login: " ,l_point2 - l_point1 )

    # id = driver.get_cookie("ZOZO%5FUID")
    return driver

def get_product(driver,url):
    print("milestone_1")
    driver.get(url)
    print("milestone_2")
    btn_add_cart = driver.find_element_by_xpath(".//form/span/input")
    btn_add_cart.click()
    print("milestone_3")
    err_msg = None
    try:
        err_msg = driver.find_element_by_xpath(".//div/section/p[@class = 'err']").get_attribute("innerHTML")
        print("Damn!", err_msg,len(err_msg))
    except:
        print("seems to be success")
    if err_msg == None:
        try:
            result = None
            result = driver.find_element_by_xpath(".//tbody/tr/td[@class = 'delete']")
            if result == None:
                print("Unknown Error")
            else:
                cookies = driver.get_cookies()
                for cookie in cookies:
                    if cookie["name"]=="ZOZO%5FUID":
                        _cookie = cookie["value"]
                    if cookie["name"][0:10] == "ASPSESSION":
                        _cookie_session = cookie["value"]
                print("ASPSESSION : ", _cookie_session, " ID : ", _cookie)
                report_to_a("ONE_CART!","URL :" + url + ">>>" +"ZOZO%5FUID : " + _cookie + " ASPSESSION : " + _cookie_session)
        except:
            print("Failed")
    # try:
    #     btn_delete = driver.find_element_by_xpath(".//tr/td[@class = 'delete']/a")
    #     print(btn_delete.get_attribute("innerHTML"))
    #     cookies = driver.get_cookies()
    #     for cookie in cookies:
    #         if cookie["name"]=="ZOZO%5FUID":
    #             _cookie = cookie["value"]
    #         if cookie["name"][0:10] == "ASPSESSION":
    #             _cookie_session = cookie["value"]
    #     print("ASPSESSION : ", _cookie_session, " ID : ", _cookie)
    #     report_to_a("ONE_CART!","URL :" + url + ">>>" +"ZOZO%5FUID : " + _cookie + " ASPSESSION : " + _cookie_session)
    # except:
    #     try:
    #         err_msg = driver.find_element_by_xpath(".//div/section/p[@class = 'err']").get_attribute("innerHTML")
    #         print("Damn!", err_msg,len(err_msg))
    #     except:
    #         print("unknown error")

def foo():
    time_start = time.time()
    # driver, _cookie, _cookie_session = Create_Driver("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2")
    print("milestone_-3")
    x = 0
    while True:
        print("milestone_-2")
        if time.time()-time_start>=600:
            break
        try:
            print("milestone_-1")
            default_driver.get("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2")
            time.sleep(1)
            products = default_driver.find_elements_by_xpath(".//li/div/a")
            print(len(products))
            url = products[x+20].get_attribute("href")
            put_in_queue(url, x)
            multi_thread()
            # get_product(get_driver, url)
            x = x +1
            if x == 5:
                x = 0
        except:
            print("getting new product failed")
            continue
        # print("milestone_-1")
        # default_driver.get("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2")
        # time.sleep(1)
        # products = default_driver.find_elements_by_xpath(".//li/div/a")
        # print(len(products))
        # url = products[x+20].get_attribute("href")
        # get_product(working_drivers[x], url)
        # x = x +1
        # if x == 3:
        #     x = 0
q = queue.LifoQueue()
default_driver = Log_in()
get_driver = Create_Driver("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2")
working_drivers = list()
for i in range(5):
    working_drivers.append(Create_Driver("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2"))
foo()

# driver = Log_in()
# driver.get("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2")
# get_product(driver)

