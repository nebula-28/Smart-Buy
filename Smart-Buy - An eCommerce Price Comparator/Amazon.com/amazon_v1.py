#Amazon Code

#main program
import requests #This will allow to send HTTP requests.
import re   #This is to import regular expression module.
import time  #This module will help to use sleep().
from bs4 import BeautifulSoup  #This is to import BeautifulSoup which will help to extract data from websites.
import sys
HEADERS={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
product_price_list=[]

def clean_prod_name(usr_typed_name):
    usr_string=re.sub('\s+',' ',re.sub('[^A-Za-z0-9]', ' ', str(usr_typed_name))) #This will remove unwanted special symbols from user given string
    return usr_string

def get_product_link(product_name):
    prod_name=product_name.replace(' ','%20')
    pName1=product_name.replace(' ','-')
    pName2=product_name.replace(' ','+')
    
    #Search Results of product typed will be shown on the below links
    am_url=f'https://www.amazon.in/{pName1}/s?k={pName2}'
    #print(fk_url)
    return am_url

def get_soup_object(url):

    web_page_request=requests.get(url,headers=HEADERS)    #Requesting HTML of the searched product
    soup_object=BeautifulSoup(web_page_request.content,'html5lib')    #Creating Soup Object on the HTMl and parsing it with html5lib
    #print(soup_object.prettify())   #Will create pretty display of the HTML tree
    return soup_object

def amazon(am_soup,product_name):
    found_flag=0
    usr_sort_list=product_name.lower().split(' ')
    #print(usr_sort_list)
    usr_sort_list.sort()
    for i in am_soup.find_all('span',attrs={'class':'a-size-medium a-color-base a-text-normal'}) or am_soup.find_all('span',attrs={'class':'a-size-base-plus a-color-base a-text-normal'}):
        html_prod_name=i.text  #This is product name given on the website
        html_prod_name1=(clean_prod_name(html_prod_name)).lower()   #This is product name after cleaning the special symbols
        am_sort_list=html_prod_name1.split()  #This will break down the actual name of product given on website
        am_sort_list.sort()
        rank=0
        for j in usr_sort_list :      #Here we will match the product name that user has given with the one that is matching with the website products
            if j in am_sort_list:
                rank=rank+1
                if rank>=2:
                    print(f"Product found on the basis of your search is : {html_prod_name}")
                    found_flag=1
                    break
                #else rank<=1->random search 
        if found_flag==1:
            prod_link='https://www.amazon.in/'+str(i.parent.get('href'))
            print("---------------------------------------",prod_link)
            return prod_link
        else:
            print("Product you are looking for is not found ! ") 
            break 


#Product Specs

def product_sepcification(am_prod_link):
    if am_prod_link!=None:
        am_soup2=get_soup_object(am_prod_link)
    else:
        pass          #Amazon Soup Object

   
    print('Amazon Specs')
    #Exrtracting Product Price
    try:
        product_price = am_soup2.find('span',attrs={'id': (re.compile('price$'))}).get_text(strip=True)
        print("Price of Product is : ",end='')
        print(product_price.replace(',',''))          
    except AttributeError:
        title_string = "NA"
        print("Product Price = ", title_string)
    #Extracting Product Review
    try:
        rating = am_soup2.find("span", attrs={'class': 'a-icon-alt'}).string
        print("Overall Rating of the product is : ",end='')
        print(rating)
    except AttributeError:
        rating="NA"
        print("Overall rating = ", rating)






#Driver Code

#The user will provide product name
usr_typed_name=input('Please Enter Product Name : ')
if len(usr_typed_name)==0 or usr_typed_name.isspace()==True  :  sys.exit("No Product Entered.Terminating the Search......")

#The below method will clean any unwanted special symbols
product_name=clean_prod_name(usr_typed_name)

#Urls for searched products 
am_url=get_product_link(product_name)
print("Searching your product in the below links.............")
print("Amazon Search Results :           ",am_url)



print("Searching best match of your product in the above links.............")
#Creating Beautiful Soup objects for all the urls 

am_soup=get_soup_object(am_url)  #Amazon Soup Object



am_prod_link=amazon(am_soup,product_name)


#Product Links are listed below:
print("Amazon Product Link :           ",am_prod_link)

#Product Specifications:
product_sepcification(am_prod_link)
