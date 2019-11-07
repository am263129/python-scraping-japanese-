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
        

def put_in_queue(urls):
    # for i in range(0, len(urls)):
    #     q.put([urls[i], global_drivers[i]])

    q.put(["https://zozo.jp/shop/zozoused/goods/42842662/?did=71213285",global_drivers[0]])
    q.put(["https://zozo.jp/shop/zozoused/goods/39677907/?did=66800870",global_drivers[1]])
    q.put(["https://zozo.jp/shop/zozoused/goods/42846748/?did=71217396",global_drivers[2]])
    q.put(["https://zozo.jp/shop/zozoused/goods/42714858/?did=71046035",global_drivers[3]])
    q.put(["https://zozo.jp/shop/zozoused/goods/42712947/?did=71044124",global_drivers[4]])
    print("put end",q)

def thread_cart():
    if q.empty():
        print("Empty Queue")
        
    while not q.empty():
    	
        value = q.get()
        print(value)
        print(value[0])
        # driver = Log_in()
        point_10 = time.time()
        driver = value[1]
        driver.get(value[0])
        
        # driver = Create_Driver(value[0])
        point_11 = time.time()
        print("get cookies")
        print("time to get: ", point_11-point_10)
        cookies = driver.get_cookies()
        print(cookies)
        for cookie in cookies:
            if cookie["name"]=="ZOZO%5FUID":
                _cookie = cookie["value"]
            if cookie["name"][0:10] == "ASPSESSION":
                _cookie_session = cookie["value"]
        try:
            print("cookie: " + str(len(cookies)))
            btn_cart = driver.find_element_by_xpath(".//form/span/input")
            btn_cart.click()
            print("Clicked button")
            err_msg = driver.find_element_by_id("secMsg")
            if err_msg == None:
                report_to_a("carted cookies","URL :" + value[0] + ">>>" +"ZOZO%5FUID : " + _cookie + " ASPSESSION : " + _cookie_session)
                print("CARTED! : zozouid : " + _cookie)
                print("          ASPSESSION: " + _cookie_session)
            else:
                print("other bot already added to cart!")

        except:
            print("Failed to add to cart")
        q.task_done()

def multi_thread(items_ids_to_cart,q):
    put_in_queue(items_ids_to_cart)
    for i in range(5):
        print("Start one thread")
        t1 = Thread(target = thread_cart)
        print("Started one thread")
        t1.start()
    q.join()
    # if len(items_ids_to_cart) < limit+1:
    #     put_in_queue(items_ids_to_cart)
    #     for i in range(len(items_ids_to_cart)):
    #         print("Start one thread")
    #         t1 = Thread(target = thread_cart)
    #         print("Started one thread")
    #         t1.start()
    #     q.join()
        # reset_product()
     
     
    

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
    # prefs = {
	# "profile.managed_default_content_settings.images":2,
	# "--disable-bundled-ppapi-flash":1
	# }
	# chromeOptions = webdriver.ChromeOptions()
    # options = Options()
    # options.add_argument('--disable-logging')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_experimental_option("prefs", prefs)
    options = Options()
    print("start_driver")
    # driver = webdriver.Chrome("/root/ragtag/chromedriver", chrome_options = options)
    driver = webdriver.Chrome("chromedriver", chrome_options = options)
    print("started driver")
    driver.get(url)
    return driver
	
    
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
    # driver.get(url)
    # return driver


def create_sec_driver():
    # prefs = {
	# "profile.managed_default_content_settings.images":2,
	# "--disable-bundled-ppapi-flash":1
	# }
	# # chromeOptions = webdriver.ChromeOptions()
    # options = Options()
    # options.add_argument('--disable-logging')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_experimental_option("prefs", prefs)
    print("start_driver")
    # driver = webdriver.Chrome("/root/ragtag/chromedriver", chrome_options = options)
    options = Options()
    driver = webdriver.Chrome("chromedriver", chrome_options = options)
    	
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

def init_product():
    current_product = list()
    while True:
        try:
            print("try to get product")
            start = timeit.default_timer()
            # global product_driver
            product_driver.get("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2")
            time.sleep(5)
            print("get finished")        
            products = product_driver.find_elements_by_xpath(".//li/div/a")
            print("get element finished",len(products))
            for x in range(0, len(products)):
                # print(products[x].get_attribute("href"))
                current_product.append(products[x].get_attribute("href"))
            point1 = timeit.default_timer()    
                            
            # page = requests.get('https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2')

            # point1 = timeit.default_timer()
            # page_byte = page.content.decode("utf-8","ignore")
            # page_string = page_byte.split('<section id="result">')[1].split('</section>')[0]
            # page_source = page_string.replace(" ","").replace("\t","").replace("\r","").replace("\n","")
            # page_href = page_source.split('catalog-link"href="')
            # for x in range(1, len(page_href)):
            #     current_product.append(page_href[x].split('"><figureclass=')[0])
            print(len(current_product))
            print("time :", point1 - start)
            break
        except:
            print("failed getting product")
            time.sleep(3)

    return current_product

def reset_product():
    global product
    product = init_product()
    
def foo(product,q):
    time_start = time.time()
    while True:
        if time.time()-time_start>=600:
            break
        try:
            compare(product,init_product())
            new_product = list()
            # new_product = compare(product,init_product())
        except:
            print("getting new product failed")
            continue
        if len(new_product) > 0:
            multi_thread(new_product,q)
        else:
            print("nothing new")
            pass
		
    # print(time.ctime())
    # threading.Timer(20, foo).start()
    # global product
    # if len(product) > 0:
    #     compare(product,init_product())
    # else:
    #     product = init_product()

def Diff(li1, li2): 
    return (list(set(li1) - set(li2)))

def compare(product, current_product):
    point7 = timeit.default_timer()
    new_product = Diff(current_product,product)
    point8 = timeit.default_timer()
    print("Runtime for get new product:", point8-point7)
    print(new_product)
    multi_thread(current_product,q)
    # return new_product
    # if (len(new_product)>0):
    #     print("Starting Multi Thread")
    #     multi_thread(new_product,q)
    #     print("Started Multi Thread")

# driver.get("https://zozo.jp/search/?sex=women&price=proper&p_ssy=2019&p_ssm=10&p_ssd=7&p_sey=2019&p_sem=10&p_sed=7&p_gtype=2")

first = 1
cookie_header = ""
global_drivers = []
global_cookie = []
global_cookie_session = []
limit = 5
for x in range(limit):
	global_drivers.append(create_sec_driver())


q = queue.LifoQueue()
product_driver = Log_in()
product = init_product()
foo(product, q)


    