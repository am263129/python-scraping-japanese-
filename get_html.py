from lxml import html
import requests
import codecs
import timeit
import time, threading
import queue,sys,subprocess
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

def get_product_list():
    point3 = timeit.default_timer()
    l_point1 = time.time()
    page = requests.get('https://zozo.jp/search/?sex=women&price=proper&p_ssy=2019&p_ssm=10&p_ssd=7&p_sey=2019&p_sem=10&p_sed=7&p_gtype=2')
    point4 = timeit.default_timer()
    l_point2 = time.time()
    page_byte = page.content.decode("utf-8","ignore")
    page_string = page_byte.split('<section id="result">')[1].split('</section>')[0]
    page_source = page_string.replace(" ","").replace("\t","").replace("\r","").replace("\n","")
    page_href = page_source.split('catalog-link"href="')
    product = list()
    point5 = timeit.default_timer()
    for x in range(1, len(page_href)):
        product.append(page_href[x].split('"><figureclass=')[0])
    point6 = timeit.default_timer()
    print("Runtime for get page:", point4 - point3)
    print("Runtime for get page_2:", l_point2 - l_point1)
    print("Runtime for get item url :", point6 - point4)
    return product
def foo():
    print(time.ctime())
    threading.Timer(10, foo).start()
    compare(product,get_product_list())
def Diff(li1, li2): 
    return (list(set(li1) - set(li2)))
def create_driver(url):
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    chrome_option.add_argument('--disable-infobars')
    chrome_option.add_argument('--disable-extensions')
    chrome_option.add_argument('--profile-directory=default')
    chrome_option.add_argument('--incognito')
    chrome_option.add_argument('--disable-plugin-discovery')
    chrome_option.add_argument('--start-maximized')

    driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options = chrome_option)
    driver.get(url)
    print("get driver")
    cookies = driver.get_cookies()
    print("get cookies")
    for cookie in cookies:
        if cookie["name"]=="ZOZO%5FUID":
            wanted_cookie = cookie["value"]
            print(cookie["name"],"=",cookies["value"])

    return driver, cookie, cookies
def compare(product, current_product):
    point7 = timeit.default_timer()
    new_product = Diff(current_product,product)
    point8 = timeit.default_timer()
    print("Runtime for get new product:", point8-point7)
    print(new_product)
    if (len(new_product)>0):
        multi_thread(new_product,q)
        print("Multi thread will run!")

def put_in_queue(elements):
    for item_id in elements:
        q.put([create_session(),"https://zozo.jp%s"%item_id])       

def create_session():
	headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language':'en-US,en;q=0.5',	
	'DNT':'1',
	'Connection':'keep-alive',
	'Upgrade-Insecure-Requests':'1'
	}
	s = HTMLSession()
	s.headers.update(headers)
	return s

def add_to_cart(session, item_url):
    print(item_url)
    driver,wanted_cookie,cookies= create_driver(item_url)
    btn_add_to_cart = driver.find_elements_by_xpath(".//form/span/input")
    for btn in btn_add_to_cart:
        btn.click()

def thread_cart():
    while not q.empty():
        value = q.get()
        print(value)
        add_to_cart(value[0], value[1])
        q.task_done()


def multi_thread(items_ids_to_cart,q):
	put_in_queue(items_ids_to_cart)
	for i in range(len(items_ids_to_cart)): 
		t1 = Thread(target = thread_cart) 
		t1.start() 	
	q.join()


start = timeit.default_timer()
page = requests.get('https://zozo.jp/search/?sex=women&price=proper&p_ssy=2019&p_ssm=10&p_ssd=7&p_sey=2019&p_sem=10&p_sed=7&p_gtype=2')
tree = html.fromstring(page.content)
point1 = timeit.default_timer()
page_byte = page.content.decode("utf-8","ignore")
page_string = page_byte.split('<section id="result">')[1].split('</section>')[0]
page_source = page_string.replace(" ","").replace("\t","").replace("\r","").replace("\n","")
page_href = page_source.split('catalog-link"href="')
point2 = timeit.default_timer()
product = list()
for x in range(1, len(page_href)):
    product.append(page_href[x].split('"><figureclass=')[0])
stop = timeit.default_timer()
print(product)
print(len(product))
print(point1-start,point2-point1,stop-point2,stop-start)
q = queue.LifoQueue()
# s = create_session()
foo()






