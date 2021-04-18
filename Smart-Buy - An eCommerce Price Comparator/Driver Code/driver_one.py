#main program
import requests #This will allow to send HTTP requests.
import re   #This is to import regular expression module.
import time  #This module will help to use sleep().
from bs4 import BeautifulSoup  #This is to import BeautifulSoup which will help to extract data from websites.
import sys


HEADERS={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

def clean_prod_name(usr_typed_name):
    usr_string=re.sub('\s+',' ',re.sub('[^A-Za-z0-9]', ' ', str(usr_typed_name))) #This will remove unwanted special symbols from user given string
    return usr_string

def get_product_link(product_name):
    prod_name=product_name.replace(' ','%20')
    pName1=product_name.replace(' ','-')
    pName2=product_name.replace(' ','+')
    
    #Search Results of product typed will be shown on the below links
    fk_url=f'https://www.flipkart.com/search?q={prod_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    am_url=f'https://www.amazon.in/{pName1}/s?k={pName2}'
    sc_url=f'https://www.shopclues.com/search?q={prod_name}&sc_z=2222&z=0&count=3&user_id=&user_segment=default'
    rd_url=f'https://www.reliancedigital.in/search?q={prod_name}:relevance'
    #print(fk_url)
    return am_url,fk_url,rd_url,sc_url

def get_soup_object(url):

    web_page_request=requests.get(url,headers=HEADERS)    #Requesting HTML of the searched product
    soup_object=BeautifulSoup(web_page_request.content,'html5lib')    #Creating Soup Object on the HTMl and parsing it with html5lib
    #print(soup_object.prettify())   #Will create pretty display of the HTML tree
    return soup_object

def Amazon(am_url):
    pass

def Flipkart(fk_url):
    pass

def Reliance_Digital(rd_url):
    pass

def Shop_Clues(sc_url):
    pass


#Driver Code

#The user will provide product name
usr_typed_name=input('Please Enter Product Name : ')
if len(usr_typed_name)==0 or usr_typed_name.isspace()==True  :  sys.exit("No Product Entered.Terminating the Search......")

#The below method will clean any unwanted special symbols
product_name=clean_prod_name(usr_typed_name)

#Urls for searched products 
am_url,fk_url,rd_url,sc_url=get_product_link(product_name)
print("Searching your product in the below links.............")
time.sleep(1)
print("Amazon Search Results :           ",am_url)
print("Flipkart Search Results :         ",fk_url)
print("Reliance Digital Search Results : ",rd_url)
print("Shop Clues Search Results :       ",sc_url)

#Creating Beautiful Soup objects for all the urls 
fk_soup=get_soup_object(fk_url)  #Flipkart Soup Object
am_soup=get_soup_object(am_url)  #Amazon Soup Object
sc_soup=get_soup_object(sc_url)  #Shop Clues Soup Object
rd_soup=get_soup_object(rd_url)  #Reliance Digital Soup Object



#product_link=find_product_in_page(fk_soup,product_name)
#print(product_link)
#product_specs(product_link)
