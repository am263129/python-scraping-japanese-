import queue,sys,subprocess
from threading import Thread
import os,time,traceback,json
import logging
import time
import csv
from datetime import datetime
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from requests_html import HTMLSession
from requests_html import HTML
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.support.ui import Select
		

def create_driver():
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
	driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)	
	driver.get("https://ntrl.ntis.gov/NTRL")
	cookies = driver.get_cookies()

	return driver
	
	
		
def report_to_w(filename,data):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "%s.txt") %filename,"w") as f:
        f.write(data)
		
def report_to_a(filename,data):
    with open("%s.csv"%filename,"a") as f:
        f.write(data)

def kill_other_self_proc():
	proc_ids_list = subprocess.check_output("ps aux | grep '%s' | awk '{print $2}'"%sys.argv[0], shell=True).split("\n")
	proc_id = str(os.getpid())
	for pid in proc_ids_list:	
		if proc_id!=pid:
			os.system("kill %s"%pid)

def get_search_link(search_link_file):
	with open(search_link_file,"r") as f:
		return f.read()

def kill_other_self_proc():
	proc_ids_list = subprocess.check_output("ps aux | grep '%s' | awk '{print $2}'"%sys.argv[0], shell=True).decode().split("\n")	
	proc_id = str(os.getpid())	
	for pid in proc_ids_list:		
		if proc_id!=pid:
			os.system("kill %s"%pid)		

print("Start")
os.system("pkill chromedriver")			
os.system("pkill chromium-browse")	
##SEARCH_LINK = get_search_link("/var/www/html/ragtag/SearchLink.txt").strip()
SEARCH_LINK = "https://ntrl.ntis.gov/NTRL"
CART_POST_LINK = "https://www.ragtag.jp/products/detail.php?"
#report_to_a('/var/www/html/tank/results','</br>## Results of Execution : <font color="#33CCFF">%s</font> ##</br></br> '%str(datetime.today())[:19])
print("Creating driver")
driver= create_driver()
print("Created driver")
##q = queue.LifoQueue()
##s = create_session()

##total_items_ids = save_initial_products(s,SEARCH_LINK)

# for i in range (0,12):
	# total_items_ids.remove(total_items_ids[i])
##print(len(total_items_ids))
##cart_new_items(s,total_items_ids,q,SEARCH_LINK)
##input = driver.find_element_by_id("advSearchForm:advancedSearchText")
##driver.execute_script("arguments[0].setAttribute('value', 'tank')", input);

driver.execute_script("document.getElementById('advSearchForm:FromYear_input').value='2018';");
driver.execute_script("document.getElementById('advSearchForm:ToYear_input').value='2019';");

numberperpage = 100

time.sleep(2)

driver.find_element_by_id("advSearchForm:advSearchSubmit").click()

time.sleep(3)

#driver.find_element_by_xpath("//select[@name='searchResultsForm:searchResultsTable_rppDD']").select_by_value = numberperpage
#driver.find_element_by_xpath("//select[@name='searchResultsForm:searchResultsTable_rppDD']").value = numberperpage

select = Select(driver.find_element_by_xpath("//select[@name='searchResultsForm:searchResultsTable_rppDD']"))
select.select_by_value(str(numberperpage)) 

#driver.find_element_by_xpath('//a[@aria-label="Next Page"]').click()
page_no = 0

for k in range (1, page_no+1):
	try:
		print("Navigate page: " + str(k))
		driver.find_element_by_xpath('//a[@aria-label="Next Page"]').click()
		time.sleep(3)
		html = HTML(html=driver.page_source)
	except:
		print("Error: next page")
		break

while True:	
	time.sleep(3)
	html = HTML(html=driver.page_source)
	
	start_num = int(driver.find_element_by_xpath('//tr[@class="ui-widget-content ui-datatable-odd ui-datatable-selectable"]').get_attribute("data-ri")) - 1
	print("Start page: " + str(start_num))

	print(numberperpage,start_num)
	for i in range (start_num, start_num+numberperpage):				
		
		try:
			
			driver.find_element_by_xpath('//tr[@data-ri="' + str(i) + '"]/td[5]/a[1]').click()
			print("clicked")
		except:
			print("Error: Downloading pdf")


	page_no = page_no + 1

	if page_no > 68:
		break

	print("Page No : " + str(page_no))

	try:
		driver.find_element_by_xpath('//a[@aria-label="Next Page"]').click()
	except:
		break

os.system("pkill chromedriver")			
os.system("pkill chromium-browse")
os.system("pkill python")