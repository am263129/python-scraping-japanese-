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

have_done = 1
first = 1
cookie_header = ""

def report_to_a(filename,data):
    with open("%s.txt"%filename,"a") as f:
        f.write(data)

def put_in_queue(elements):
    for item_id in elements:
        q.put("https://zozo.jp%s"%item_id)
    # q.put("https://zozo.jp%s"%elements[5])
    # q.put("https://zozo.jp%s"%elements[6])
    # q.put("https://zozo.jp%s"%elements[7])
    # q.put("https://zozo.jp%s"%elements[8])
    # q.put("https://zozo.jp%s"%elements[9])

def thread_cart():
    while not q.empty():
        value = q.get()
        print(value)
        driver = Log_in()
        time.sleep(30)
        driver.get(value)
        cookies = driver.get_cookies()
        print("get cookies")
        for cookie in cookies:
        	if cookie["name"]=="ZOZO%5FUID":
        		_cookie=cookie["value"]
                
        try:
            btn_cart = driver.find_element_by_xpath(".//form[@action = '/_cart/default.html']/span/input")
            btn_cart.click()
            print(_cookie)
            report_to_a("carted cookies",_cookie)
            
        except:
            print("Failed to add to cart")
        # driver.close()
        q.task_done()

def multi_thread(items_ids_to_cart,q):
	put_in_queue(items_ids_to_cart)
	for i in range(5): 
		t1 = Thread(target = thread_cart) 
		t1.start()  
	q.join()
    

def Create_Driver(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=default')
    options.add_argument('--incognito')
    options.add_argument('--disable-plugin-discovery')
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(executable_path="chromedriver", chrome_options = options)
    
    # prefs = {
    # "profile.managed_default_content_settings.images":2,
    # "--disable-bundled-ppapi-flash":1
    # }
    # # chromeOptions = webdriver.ChromeOptions()
    # options = Options()
    # options.add_argument('--disable-logging')
    # options.add_argument('--headless')
    # options.add_argument('--disable-logging')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_experimental_option("prefs",prefs)
    # driver = webdriver.Chrome(executable_path="chromedriver", chrome_options = options)
    # driver.get("https://zozo.jp/_member/login.html?bkurl=%2F%5Fmember%2Flogin%2Ehtml%3Fbkurl%3D%252F%255Fmember%252Flogin%252Ehtml%253Fbkurl%253D%25252F%25255Fmember%25252Flogin%25252Ehtml%25253Fbkurl%25253D%2525252F%2525255Fmember%2525252Flogin%2525252Ehtml%2525253Fm%2525253Dlogout%25252526pattern%2525253D%25252526from%2525253D%25252526integrated%2525253D")
    driver.get(url)
    return driver


def create_sec_driver(url):
    prefs = {
    "profile.managed_default_content_settings.images":2,
    "--disable-bundled-ppapi-flash":1
    }
    # chromeOptions = webdriver.ChromeOptions()
    options = Options()
    options.add_argument('--disable-logging')
    options.add_argument('--headless')
    options.add_argument('--disable-logging')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path="chromedriver", chrome_options = options)
    return driver

def Log_in():
    l_point1 = time.time()
    driver = create_sec_driver("https://zozo.jp/_member/login.html?bkurl=%2F%5Fmember%2Flogin%2Ehtml%3Fbkurl%3D%252F%255Fmember%252Flogin%252Ehtml%253Fbkurl%253D%25252F%25255Fmember%25252Flogin%25252Ehtml%25253Fbkurl%25253D%2525252F%2525255Fmember%2525252Flogin%2525252Ehtml%2525253Fm%2525253Dlogout%25252526pattern%2525253D%25252526from%2525253D%25252526integrated%2525253D")
    print("get driver")
    username = driver.find_element_by_xpath(".//li[@id = 'memID']/input")
    userpassword = driver.find_element_by_xpath(".//li[@id = 'passWord']/input")
    username.send_keys("x0xenx@gmail.com")
    userpassword.send_keys("0771397840xe")
    btn_login = driver.find_element_by_xpath(".//div[@class = 'container clearfix']/p[@class = 'btn']/input")
    btn_login.click()
    l_point2 = time.time()
    print("time for login: " ,l_point2 - l_point1 )

    # id = driver.get_cookie("ZOZO%5FUID")
    return driver
    

def init_product():
    start = timeit.default_timer()
    page = requests.get('https://zozo.jp/search/?sex=women&price=proper&p_ssy=2019&p_ssm=10&p_ssd=7&p_sey=2019&p_sem=10&p_sed=7&p_gtype=2')
    # tree = html.fromstring(page.content)
    point1 = timeit.default_timer()
    page_byte = page.content.decode("utf-8","ignore")
    page_string = page_byte.split('<section id="result">')[1].split('</section>')[0]
    page_source = page_string.replace(" ","").replace("\t","").replace("\r","").replace("\n","")
    page_href = page_source.split('catalog-link"href="')
    product = list()
    for x in range(1, len(page_href)):
        product.append(page_href[x].split('"><figureclass=')[0])
    stop = timeit.default_timer()
    print(len(product))
    print("time for get_html: ", point1-start,"full time: ",stop-start)
    return product

def foo():
    print(time.ctime())
    # threading.Timer(10, foo).start()
    # global have_done
    # if have_done :
    #     global product
    #     product = init_product()
    #     have_done = 0
    compare(product,init_product())

def Diff(li1, li2): 
    return (list(set(li1) - set(li2)))

def compare(product, current_product):
    point7 = timeit.default_timer()
    new_product = Diff(current_product,product)
    point8 = timeit.default_timer()
    print("Runtime for get new product:", point8-point7)
    print(new_product)
    multi_thread(current_product,q)
    # if (len(new_product)>0):
    #     multi_thread(new_product,q)
    #     global have_done
    #     have_done = 1

# driver.get("https://zozo.jp/search/?sex=women&price=proper&p_ssy=2019&p_ssm=10&p_ssd=7&p_sey=2019&p_sem=10&p_sed=7&p_gtype=2")

Log_in()
q = queue.LifoQueue()
# cookies = driver.get_cookies()
# print("get cookies")
# for cookie in cookies:
#     if cookie["name"]=="ZOZO%5FUID":
#         wanted_cookie = cookie["value"]
#         # print(cookie["name"],"=",cookies["value"])
# btn_add_to_cart = driver.find_elements_by_xpath(".//form[@action = '/_cart/default.html']/span/input")
# print(len(btn_add_to_cart))
# multi_thread(btn_add_to_cart,q)
product = init_product()
foo()


    