#Reliance Digital Code

import requests
from bs4 import BeautifulSoup
import re

HEADERS={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

def clean_prod_name(usr):
    string1=re.sub('[^A-Za-z0-9]', ' ', str(usr))
    string2=re.sub('\s+',' ',str(string1))
    #print(string2)
    return string2

def get_rd_link(product_name):
    usr_prod_name=product_name.replace(' ','%20')
    #print(usr_prod_name)
    rd_url=f'https://www.reliancedigital.in/search?q={usr_prod_name}:relevance'
    #print(rd_url)
    return rd_url

def rd_soup_object(rd_url):
    rd_web_pg=requests.get(rd_url,headers=HEADERS)
    rd_soup1=BeautifulSoup(rd_web_pg.content,'html5lib')
    #print(rd_soup.prettify())
    return rd_soup1

def product_price(rd_soup,product_name):
    found_flag=0
    usr_sort_list=product_name.lower().split(' ')
    #print(usr_sort_list)
    usr_sort_list.sort()
    for i in rd_soup.find_all('p',attrs={'class':'sp__name'}):
        html_prod_name=i.text  #This is product name given on the website
        html_prod_name1=(clean_prod_name(html_prod_name)).lower()   #This is product name after cleaning the special symbols
        rd_sort_list=html_prod_name1.split()  #This will break down the actual name of product given on website
        rd_sort_list.sort()
        rank=0
        for j in usr_sort_list :      #Here we will match the product name that user has given with the one that is matching with the website products
            if j in rd_sort_list:
                rank=rank+1
                if rank>=2:
                    print(f"Product found on the basis of your search is : {html_prod_name}")
                    found_flag=1
                    break
                #else rank<=1->random search 
        #Finding price of the searched product
        if found_flag==1:
            link=i.parent.parent.parent.get('href')
            print(f'Product URL : https://www.reliancedigital.in{link}')
            price_ob=i.parent.find('span',attrs={'class':'sc-bdVaJa hKEXmy'})
            print("Price of Product : ",price_ob.text)
            price_of_product=re.sub('[,₹]','',price_ob.text)
            break
        else:
            print("Product you are looking for is not found ! ") 
            break
    return price_of_product

usr=input('Please Enter Product Name : ')
#Step 1 is to clean the product name to make the product search easy
product_name=clean_prod_name(usr)
#Step 2 is to get product link for the searched product
rd_url=get_rd_link(product_name)
#Step 3 is creating Soup Object
rd_soup=rd_soup_object(rd_url)
#Step 4 is to find product specs. For Reliance Digital , Customer Ratings is not avaialable . Hence we will just compare price
price_of_product=product_price(rd_soup,product_name)
print(f"Overall Rating : Not Available ★")
