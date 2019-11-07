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

def create_driver(url):
    prefs = {
        "profile.managed_default_content_settings.images":2,
	    "--disable-bundled-ppapi-flash":1
    }
    options = Options()
    options.add_argument('--disable-logging')
    options.add_argument('--headless')
    options.add_argument('--disable-logging')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs",prefs)
    print("start driver")
    point_1 = time.time()
    driver = webdriver.Chrome("chromedriver",chrome_options=options)
    point_2 = time.time()
    print("started driver")
    driver.get(url)
    point_3 = time.time()
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie["name"]=="ZOZO%5FUID":
            _cookie = cookie["value"]
        if cookie["name"][0:10] == "ASPSESSION":
            _cookie_session = cookie["value"]
    point_4 = time.time()
    print("Time create_driver : ",point_2-point_1)
    print("Time get_url : ",point_3-point_2)
    print("Time get_cookies : ",point_4-point_3)
    return driver
point_5 = time.time()
driver = create_driver("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2")
point_6 = time.time()
products = driver.find_elements_by_xpath(".//li/div/a")
point_7 = time.time()
print("Time create and get gookies : ",point_6-point_5)
print("Time get_product : ",point_7-point_6)
print("Time all : ",point_7-point_5)

          








create_driver("https://zozo.jp/shop/zozoused/goods/42927131/?did=71397977")