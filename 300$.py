from tkinter import *
from tkinter import messagebox
from requests_download import download
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import lxml.html,os,json,requests
import time
import datetime
import random
import json



def start_get_new():
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    chrome_option.add_argument('--disable-infobars')
    chrome_option.add_argument('--disable-extensions')
    chrome_option.add_argument('--profile-directory=default')
    chrome_option.add_argument('--incognito')
    chrome_option.add_argument('--disable-plugin-discovery')
    chrome_option.add_argument('--start-maximized')

    driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options = chrome_option)
    driver.delete_all_cookies()

    urls = ["https://zozo.jp/brand/studioclip/?dord=21","https://zozo.jp/brand/nanouniverse/?dord=21","https://zozo.jp/brand/nike/?dord=21"]
  
    for x in range(1, len(urls) + 1):
        driver.execute_script("window.open();")
        driver.switch_to.window(driver.window_handles[x])
        driver.get(urls[x - 1])

start_get_new()