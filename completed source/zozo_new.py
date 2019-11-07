import requests
from lxml import html
import time
import traceback
from threading import Thread

def create_session():
    session = requests.Session()
    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1'
    }	
    session.headers.update(headers)	
    return session

def get_payload(username,password):
    return {
            "c":"Login",	
            "memid":username,
            "mempw":password,
            "autologin":"1",
            "pattern":""
    }
def while_request_tree(session,link):	
	while True:
		try:
			r =  session.get(link)
			if r.url=="https://img4.zozo.jp/sorry/sorry.html":
				print( "while_request_tree sorry page detected passing..." )
				time.sleep(1)
				pass
			else:
				return r,html.fromstring(r.text)
		except:
			print( "request error for link : %s \n%s\nretrying..."%(link,traceback.format_exc()) )
			time.sleep(1)

def while_request_tree_post(session,link,payload):
    while True:
        try:		
            r = session.post(link,data=payload)
            if r.url=="http://img4.zozo.jp/sorry/sorry.html":
                print( "while_request_tree_post sorry page detected passing..." )
                time.sleep(1)
                continue
            else:
                return r
        except:
            print ("request error for link : %s \n%s\nretrying..." % ( link, traceback.format_exc()) )
            time.sleep(1)

def singed_in(r):
	if not "c=logout" in r.text:
		print( "Failed Logout where c=logout" )
	return "c=logout" in r.text

def post_request(session,login_url,payload):
    post_headers={
                'Host':'zozo.jp',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'en-US,en;q=0.5',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive',
                'Upgrade-Insecure-Requests':'1'
                }
    session.headers.update(post_headers)
    r = while_request_tree_post(session,login_url,payload)	
    # save_page("login",r.text)
    return singed_in(r)

def threading(items_to_cart):
	for itemid in items_to_cart:
		t1 = Thread(target = do_work, args=(itemid,))
		t1.start()

def login(session,login_url,username,password):
    return session

    session.get(login_url)
    data = get_payload(username,password)
    if post_request(session,login_url,data):
        print ("Login Successful")
        return session
    else:
        exit("Can't login")

def do_work(itemid):
    try:
        session = create_session()
        session.headers.update(s.headers)
        session.cookies.update(s.cookies)
        main_work(session,itemid)
    except:
        if "Duplicate" not in traceback.format_exc():
            print( "\n\nscrape Function failed Error = %s"%traceback.format_exc() )
        else: print( "Duplicate" )
    
    try:session.close()
    except:pass

def get_hidden_input(tree,input_name):
    try:
        return tree.xpath('//input[@type="hidden" and @name="%s"]//@value'%input_name)[0]	
    except:
        print( traceback.format_exc() )
        return False

def get_hidden_inputs(tree,names_list):
    hidden_inputs_dict={"c":"put", "rid":""}
    for input_name in names_list:
        hidden_input_value = get_hidden_input(tree,input_name)
        if not hidden_input_value:
            print( "can't get_hidden_inputs %s"%input_name )
        hidden_inputs_dict.update({input_name:hidden_input_value})
    return hidden_inputs_dict

def main_work(session,item_id):
    print("addedcart process:",item_id)
    add_item_to_cart(session,"https://zozo.jp/shop/zozoused/goods/%s/"%item_id)

def add_item_to_cart(session,item_link):	
    r1,tree=while_request_tree(session,item_link)
    added=False
    if not tree.xpath('boolean(//form[@action="/_cart/default.html"])'):
        print( "Cart button not found, %s"%r1.url )
    else:
        payload=get_hidden_inputs(tree,["sid","p_seckey"])
        if not payload:
            print( "not_add_to_cart_%s"%item_link.split("/")[-2] )
        else:
            r = while_request_tree_post(session,add_to_cart_link,payload)
            added = "PutMessage" in r.url
            if added:
                report_to_File( session, item_link )
                pass
            else:
                print( "Not add to cart" )
                pass
def report_to_File1(data):
    with open("test.html","a") as f:
        f.write(time.ctime())
        f.write("\n")
        f.write(data)
        f.write("\n")

def report_to_File( session, item_link ):
    cookies = session.cookies.get_dict()
    for cookie_key in cookies:
        if cookie_key=="ZOZO%5FUID":
            _cookie = cookies[cookie_key]
        if cookie_key[0:10] == "ASPSESSION":
            _cookie_session = cookies[cookie_key]
    print("Added to Cart --ASPSESSION : ", _cookie_session, " ID : ", _cookie)
    writeData = "URL :" + item_link + ">>>" +"ZOZO%5FUID : " + _cookie + " ASPSESSION : " + _cookie_session

    with open(cartlist_file_name,"a") as f:
        f.write(time.ctime())
        f.write("\n")
        f.write(writeData)
        f.write("\n")

def while_request_tree_120(session,link, cnt):
    # while True:
    # 	try:
    r =  session.get( link )
    tree= html.fromstring( r.text )
    items_ids = get_item_ids( tree, cnt )
    return items_ids

def get_item_ids(tree, cnt):
    item_ids=[]
    if cnt == 120 :
        datas = tree.xpath('//li[@data-sid]//div[@class="catalog-item-container"]//a[@class="catalog-link"]//@href')
        for i in range(50,70):
            # print (item_url )
            item_ids.append(int(datas[i].split("/")[4]))
    else:
        datas = tree.xpath('//li[@data-sid]//div[@class="catalog-item-container"]//a[@class="catalog-link"]//@href')
        for i in range(cnt):
            item_ids.append(int(datas[i].split("/")[4]))
    return item_ids

def get_items_from_first_page(s,favorites_page, buf_cnt):
    print( "\n-++-+-+-+-+-get items from :%s" % favorites_page )
    items_ids =while_request_tree_120(s,favorites_page, buf_cnt)
    return items_ids


def cart_new_arrivals(s,favorites_page, buf_cnt):
    items_ids = while_request_tree_120(s,favorites_page, buf_cnt)
    # items_to_cart = ["40154806"]

    items_to_cart = list(set(items_ids).difference(buffer_itemids))
    for i in items_to_cart:
        buffer_itemids.insert(0,i)
        buffer_itemids.pop()

    print( "Items to cart : %s" % items_to_cart )
    if len(items_to_cart)!=0:
        threading(items_to_cart)





if __name__ == "__main__":
   login_url = "https://zozo.jp/_member/login.html"
   add_to_cart_link = "https://zozo.jp/_cart/default.html"
   favorites_page = "https://zozo.jp/search/?p_gtype=2&p_fblid=1&search=2"
   username = "x0xenx@gmail.com"
   password = "0771397840xe"
   cartlist_file_name = "CartList-"+time.strftime('%Y-%m-%d', time.localtime())+".txt"
   buffer_cnt = 20
   # login
   
   s = login(create_session(),login_url,username,password)
   print( "login successful" )
   
   buffer_itemids = get_items_from_first_page(s,favorites_page, 120 )
   print( buffer_itemids )
   
   print( "waiting for new items" )
   while True:
      cart_new_arrivals(s,favorites_page, buffer_cnt)



   


   
   
#    get_items_from_first_page( favorites_page )
#    print ( "waiting for new items" )




