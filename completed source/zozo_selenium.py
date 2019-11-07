import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


login_url = "https://zozo.jp/_member/login.html"
search_list_url = "https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2"
delay_time = 5
child_drivers = 5
cnt_products = 2
cartlist_file_name = "CartList-"+time.strftime('%Y-%m-%d', time.localtime())+".txt"

print( "Pool products count: ",cnt_products)
print( "Child chrome drivers: ",child_drivers)
print( "File name: ", cartlist_file_name)

def Create_Driver():
    caps = DesiredCapabilities().CHROME
    # caps["pageLoadStrategy"] = "normal"  #  complete
    caps["pageLoadStrategy"] = "none"
    
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
    print("starting driver")
    driver = webdriver.Chrome("chromedriver", options = options,desired_capabilities=caps)
    # driver = webdriver.Chrome("chromedriver")
    driver.implicitly_wait(10)
    print("started driver")
    return driver

def Log_in(url):
    driver = Create_Driver()
    while True:
        try:
            driver.get(url)
            username = driver.find_element_by_xpath("//li[@id = 'memID']/input")
            userpassword = driver.find_element_by_xpath("//li[@id = 'passWord']/input")
            username.send_keys("x0xenx@gmail.com")
            userpassword.send_keys("0771397840xe")
            btn_login = driver.find_element_by_xpath("//div[@class = 'container clearfix']/p[@class = 'btn']/input")
            btn_login.click()
            break
        except: # not found username, userpassword
            print("not found username, userpassword, login btn element")
            time.sleep(delay_time)
            continue
    return driver

def add_cart(url, driver_index):
    
    driver = working_drivers[driver_index]
    driver.get(url)
    try:
        btn_add_cart = driver.find_element_by_xpath("//form/span/input")
        print("click add_cart")
        btn_add_cart.click()
    except:
        print("not found cart btn")
        return
    # try:
    #     err_msg_element = driver.find_element_by_xpath("//div/section/p[@class = 'err']")
    #     err_msg_element.get_attribute("innerHTML")
    #     print("Already other user carted")
    #     return
    # except:
    #     print("")
    try:
        driver.find_element_by_xpath("//tbody/tr/td[@class = 'delete']")
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie["name"]=="ZOZO%5FUID":
                _cookie = cookie["value"]
            if cookie["name"][0:10] == "ASPSESSION":
                _cookie_session = cookie["value"]
        print("Added to Cart --ASPSESSION : ", _cookie_session, " ID : ", _cookie)
        report_to_File("URL :" + url + ">>>" +"ZOZO%5FUID : " + _cookie + " ASPSESSION : " + _cookie_session)
    except:
        #no addCart button in product page
        print("Can't find element //tbody/tr/td[@class = 'delete']") 
        return

def report_to_File( data ):
    with open(cartlist_file_name,"a") as f:
        f.write(time.ctime())
        f.write("\n")
        f.write(data)
        f.write("\n")

def searching_new_products():
    
    driver_index = 0
    last_products = []

    while True:
        print("getting new products...")
        logged_in_driver.get(search_list_url)
        try:
            products = logged_in_driver.find_elements_by_xpath("//li/div/a")
        except: # not found products
            print( "not found products")
            time.sleep(delay_time)
            continue
        for i in range(cnt_products):
            try:
                new_url = products[i].get_attribute("href")
                if new_url in last_products:
                    if i ==0 :
                        time.sleep(delay_time)
                        break
                    continue
                print("Get:"+new_url)
                x = threading.Thread(target=add_cart, args=(new_url, driver_index))
                x.start()

                last_products.insert(0,new_url)
                driver_index +=1
                if driver_index >= child_drivers: 
                    driver_index = 0
                
                if len(last_products)> cnt_products:
                    last_products.pop()
            except: # failed get_attribute
                print("failed to get new product href")
                # time.sleep(delay_time)
                break
print("Creating Driver for Login")
logged_in_driver = Log_in(login_url)

print("Creating Child Driver")
working_drivers = list()
for i in range(child_drivers):
    working_drivers.append(Create_Driver())

searching_new_products()