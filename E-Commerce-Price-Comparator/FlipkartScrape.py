import requests
from bs4 import BeautifulSoup
import re
HEADERS={'User-Agent': ''}

def clean_prod_name(usr):
    string1=re.sub('[^A-Za-z0-9]', ' ', str(usr))
    string2=re.sub('\s+',' ',str(string1))
    #print(string2)
    return string2

def get_fk_link(product_name):
    usr_prod_name=product_name.replace(' ','%20')
    #print(usr_prod_name)
    fk_url=f'https://www.flipkart.com/search?q={usr_prod_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    #print(fk_url)
    return fk_url

def fk_soup_object(flipkart_url):
    fk_web_pg=requests.get(flipkart_url,headers=HEADERS)
    fk_soup=BeautifulSoup(fk_web_pg.content,'html5lib')
    #print(fk_soup.prettify())
    return fk_soup

def find_product_in_page(fk_soup,product_name):
    usr_sort_list=product_name.lower().split(' ')
    #print(usr_sort_list)
    usr_sort_list.sort()
    for i in fk_soup.find_all('a',attrs={'class':'s1Q9rs'}):
        html_prod_name=i.title
        #print(html_prod_name)
        html_prod_name1=(clean_prod_name(html_prod_name)).lower()
        #print(html_prod_name1)
        fk_sort_list=html_prod_name1.split()
        #print(html_prod_name2)
        fk_sort_list.sort()
        #print(fk_sort_list)
        rank=0
        for j in usr_sort_list :
            if j in fk_sort_list:
                rank=rank+1
                print('rank : ',rank)
                if rank>2:
                    #src=fk_soup.find('')
                    #print(i.get('href'))
                    #print(i.parent.parent.parent.get('href'))
                    break
        link1=i.get('href')
        product_link='https://www.flipkart.com'+link1
        print(product_link)
        break
        
    else:
        for i in fk_soup.find_all('div',attrs={'class':'_4rR01T'}):
            html_prod_name=i.text
            #print(html_prod_name)
            html_prod_name1=(clean_prod_name(html_prod_name)).lower()
            #print(html_prod_name1)
            fk_sort_list=html_prod_name1.split()
            #print(html_prod_name2)
            fk_sort_list.sort()
            #print(fk_sort_list)
            rank=0
            for j in usr_sort_list :
                if j in fk_sort_list:
                    rank=rank+1
                    print('rank : ',rank)
                    if rank>=2:
                        #src=fk_soup.find('')
                        #print(i.get('href'))
                        #print(i.parent.parent.parent.get('href'))
                        break
            link1=i.parent.parent.parent.get('href')
            product_link='https://www.flipkart.com'+link1
            print(product_link)
            break 
        else:
            print("Product you are looking for is not found ! ")
            
        

usr=input('Please enter Product Name : ')
product_name=clean_prod_name(usr)
fk_url=get_fk_link(product_name)
fk_soup=fk_soup_object(fk_url)
find_product_in_page(fk_soup,product_name)
