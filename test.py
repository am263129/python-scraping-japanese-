from threading import Thread
from datetime import datetime
import queue,sys,subprocess
import os,time,traceback,json
from requests_html import HTMLSession
from requests_html import HTML
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import timeit
import pickle

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=default')
options.add_argument('--incognito')
options.add_argument('--disable-plugin-discovery')
options.add_argument('--start-maximized')
driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options = options)

driver.get("https://zozo.jp/_member/login.html")
time.sleep(3)
print("try to login")
username = driver.find_element_by_xpath(".//li[@id = 'memID']/input")
userpassword = driver.find_element_by_xpath(".//li[@id = 'passWord']/input")
print("getting input successful")
username.send_keys("x0xenx@gmail.com")
userpassword.send_keys("0771397840xe")
btn_login = driver.find_element_by_xpath(".//div[@class = 'container clearfix']/p[@class = 'btn']/input")
btn_login.click()
driver.get("https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2")
products = driver.find_elements_by_xpath(".//li/div/a")
print(len(products))
current_product = list()
for x in range(0, len(products)):
    current_product.append(products[x].get_attribute("href"))
# driver.delete_all_cookies()
# cookies = pickle.load(open("cookies.pkl", "rb"))
# for cookie in cookies:
#     driver.add_cookie(cookie)

