#main program
import requests #This will allow to send HTTP requests.
import re   #This is to import regular expression module.
import time  #This module will help to use sleep().
from bs4 import BeautifulSoup  #This is to import BeautifulSoup which will help to extract data from websites.
import sys

product_price_list=[]
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

def amazon(am_soup,product_name):
    found_flag=0
    usr_sort_list=product_name.lower().split(' ')
    #print(usr_sort_list)
    usr_sort_list.sort()
    for i in am_soup.find_all('span',attrs={'class':'a-size-medium a-color-base a-text-normal'}):
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
            return prod_link
        else:
            print("Product you are looking for is not found ! ") 
            break


def flipkart(fk_soup,product_name):
    found_flag=0
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
                #print('rank : ',rank)
                if rank>=2:
                    print(f"Product found on the basis of your search is : {html_prod_name}")
                    #src=fk_soup.find('')
                    #print(i.get('href'))
                    #print(i.parent.parent.parent.get('href'))
                    break
                #else rank<=1->random search 
        prod_link='https://www.flipkart.com'+str(i.get('href'))
        #print(prod_link)
        found_flag=1
        break

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
                    #print('rank : ',rank)
                    if rank>=2:
                        print(f"Product found on the basis of your search is : {html_prod_name}")
                        #src=fk_soup.find('')
                        #print(i.get('href'))
                        #print(i.parent.parent.parent.get('href'))
                        break
                    #else rank<=1->random search 
            prod_link='https://www.flipkart.com'+str(i.parent.parent.parent.get('href'))
            #print(prod_link)
            found_flag=1
            break 
    if found_flag==0:
        print("Product you are looking for is not found ! ") 
    return prod_link  

def reliance_digital(rd_soup,product_name):
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
            prod_link='https://www.reliancedigital.in'+str(i.parent.parent.parent.get('href'))
            return prod_link
        else:
            print("Product you are looking for is not found ! ") 
            break

def shop_clues(sc_soup,product_name):
    found_flag=0
    usr_sort_list=product_name.lower().split(' ')
    #print(usr_sort_list)
    usr_sort_list.sort()
    for i in sc_soup.find_all('div',attrs={'class':'column col3 search_blocks'}):
        html_prod_name=i.find('h2').text  #This is product name given on the website
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
            plink=i.find('a').get('href')
            prod_link='https:'+str(plink)
            #print(f'ShopClues URL : {prod_link}')
            #price_ob=i.find('span',attrs={'class':'p_price'})
            #print("Price of Product : ",price_ob.text)
            #price_of_product=re.sub('[,₹]','',price_ob.text)
            #print(f"Overall Rating : Not Available ★")
            return prod_link
        else:
            print("Product you are looking for is not found ! ") 
            break

#Product Specs

def product_sepcification(fk_prod_link,am_prod_link,sc_prod_link,rd_prod_link):
    if fk_prod_link!=None :
        fk_soup2=get_soup_object(fk_prod_link) 
    else:
        pass          #Flipkart Soup Object 
     
    if am_prod_link!=None:
        am_soup2=get_soup_object(am_prod_link)
    else:
        pass          #Amazon Soup Object
     
    if sc_prod_link!=None:
        sc_soup2=get_soup_object(sc_prod_link) #Shop Clues Soup Object
    else:
        pass 
    if rd_prod_link!=None:
        rd_soup2=get_soup_object(rd_prod_link)          #Reliance Digital Soup Object  
    else:
        pass 
   
##########################################################################   
    print('Flipkart Specs')
    #Exrtracting Product Price
    try:
        product_price =re.sub('[,₹]','',fk_soup2.find("div", attrs={'class': '_30jeq3'}).string)
        print(f"Product Price :₹{product_price}")
    except AttributeError:
        title_string = "NA"
        print("Product Price = ", title_string)

    #Extracting Product Review
    try:
        rating = fk_soup2.find("div", attrs={'class': '_3LWZlK'}).text
        print(f"Overall Rating : {rating} ★")
    except AttributeError:
        rating="NA"
        print("Overall Rating = ", rating)
##########################################################################
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
############################################################################
    print('Reliance Digital Specs')
    #Exrtracting Product Price
    try:
        price_ob=rd_soup2.parent.find('span',attrs={'class':'sc-bdVaJa hKEXmy'})
        print("Price of Product : ",price_ob.text)
        price_of_product=re.sub('[,₹]','',price_ob.text)
    except AttributeError:
        title_string = "NA"
        print("Product Price = ", title_string)
    

    #Extracting Product Review
    print(f"Overall Rating : Not Available ★")
#############################################################################
    print('Shopclues Specs')
    #Exrtracting Product Price
    #try:
    product_price =re.sub('[,₹Rs.]','',sc_soup2.find("span", attrs={'class': 'f_price'}).text)
    print('')
    print(f"Product Price :₹{product_price}")
    #except AttributeError:
        #title_string = "NA"
        #print("Product Price = ", title_string)

    #Extracting Product Review
    try:
        #rating = sc_soup2.find("div", attrs={'class': 'ratings'}).contents
        rating = sc_soup2.find("span", attrs={'class': 'val'}).text
        print(f"Overall Rating : {rating} ★")
    except AttributeError:
        rating="NA"
        print("Overall Rating = ", rating)   



#Driver Code

#The user will provide product name
usr_typed_name=input('Please Enter Product Name : ')
if len(usr_typed_name)==0 or usr_typed_name.isspace()==True  :  sys.exit("No Product Entered.Terminating the Search......")

#The below method will clean any unwanted special symbols
product_name=clean_prod_name(usr_typed_name)

#Urls for searched products 
am_url,fk_url,rd_url,sc_url=get_product_link(product_name)
print("Searching your product in the below links.............")
print("Amazon Search Results :           ",am_url)
print("Flipkart Search Results :         ",fk_url)
print("Reliance Digital Search Results : ",rd_url)
print("Shop Clues Search Results :       ",sc_url)

print("Searching best match of your product in the above links.............")
#Creating Beautiful Soup objects for all the urls 
fk_soup=get_soup_object(fk_url)  #Flipkart Soup Object
am_soup=get_soup_object(am_url)  #Amazon Soup Object
sc_soup=get_soup_object(sc_url)  #Shop Clues Soup Object
rd_soup=get_soup_object(rd_url)  #Reliance Digital Soup Object

fk_prod_link=flipkart(fk_soup,product_name)
am_prod_link=amazon(am_soup,product_name)
sc_prod_link=shop_clues(sc_soup,product_name)
rd_prod_link=reliance_digital(rd_soup,product_name)

#Product Links are listed below:
print("Amazon Product Link :           ",am_prod_link)
print("Flipkart Product Link :         ",fk_prod_link)
print("Reliance Product Link :         ",rd_prod_link)
print("Shop Clues Product Link :       ",sc_prod_link)


#Product Specifications:
product_sepcification(fk_prod_link,am_prod_link,sc_prod_link,rd_prod_link)
