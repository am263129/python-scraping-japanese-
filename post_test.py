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



# page = requests.get('https://zozo.jp/shop/zozoused/goods/42927131/?did=71397977')
# page_byte = page.content.decode("utf-8","ignore")
# sid = page_byte.split('"sid" value="')[1].split('" />')[0]
# rid = page_byte.split('"rid" value="')[1].split('" />')[0]
# p_seckey = page_byte.split('"p_seckey" value="')[1].split('" />')[0]
# # page_string = page_string.split('" />')[0]
# print(sid, rid, p_seckey)
def create_driver(url):
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
	print("start driver")
	driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)	
	print("started driver")
	driver.get(url)	
	print("get driver")
	cookies = driver.get_cookies()
	print("get cookies")
	for cookie in cookies:
		if cookie["name"]=="ECSESSID":
			print(cookie["name"],"=",cookie["value"])
	return driver,cookies

def get_post_data(item_url):
    page = requests.get(item_url)
    page_byte = page.content.decode("utf-8","ignore")
    sid = page_byte.split('"sid" value="')[1].split('" />')[0]
    rid = page_byte.split('"rid" value="')[1].split('" />')[0]
    p_seckey = page_byte.split('"p_seckey" value="')[1].split('" />')[0]
    # page_string = page_string.split('" />')[0]
    return{
        "c" : "put",
        "sid" : sid,
        "rid" : rid,
        "p_seckey" : p_seckey
    }
def create_session(cookies):
	headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language':'en-US,en;q=0.5',	
	'DNT':'1',
	'Connection':'keep-alive',
	'Upgrade-Insecure-Requests':'1',
    'Cookies':'ZOZO%5FUID=P9203%3A478469323%3A623826524;'
	}
	s = HTMLSession()
	s.headers.update(headers)	
	# for cookie in cookies:
		# s.cookies.set(cookie['name'], cookie['value'])
	# report_to_w("initial_cookies",str(dict(s.cookies)))
	return s    
def post_request_block(session,link,post_data):	
	while True:
		try:
			r =  session.post(link,data=post_data)
			return r
		except:
			print("request error for link failed")
			time.sleep(1)


result = get_post_data("https://zozo.jp/shop/zozoused/goods/42927131/?did=71397977")
driver,cookies = create_driver("https://zozo.jp/shop/zozoused/goods/42927131/?did=71397977") 
session = create_session(cookies)
response = post_request_block(session,"https://zozo.jp/_cart/default.html",result)   
print(response)
