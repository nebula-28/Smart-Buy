import requests
from bs4 import BeautifulSoup
import re
HEADERS={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

def clean_prod_name(usr):
    string1=re.sub('[^A-Za-z0-9]', ' ', str(usr))
    string2=re.sub('\s+',' ',str(string1))
    #print(string2)
    return string2

def get_sc_link(product_name):
    usr_prod_name=product_name.replace(' ','%20')
    #print(usr_prod_name)
    sc_url=f'https://www.shopclues.com/search?q={usr_prod_name}&sc_z=2222&z=0&count=3&user_id=&user_segment=default'
    #print(sc_url)
    return sc_url

def sc_soup_object(sc_url):
    sc_web_pg=requests.get(sc_url,headers=HEADERS)
    sc_soup1=BeautifulSoup(sc_web_pg.content,'html5lib')
    #print(sc_soup.prettify())
    return sc_soup1

def get_product_link(sc_soup,product_name):
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
            print(f'Product URL : {prod_link}')
            #price_ob=i.find('span',attrs={'class':'p_price'})
            #print("Price of Product : ",price_ob.text)
            #price_of_product=re.sub('[,₹]','',price_ob.text)
            #print(f"Overall Rating : Not Available ★")
            return prod_link
        else:
            print("Product you are looking for is not found ! ") 
            break

def product_specs(product_link):
    sc_soup2=sc_soup_object(product_link)
    #print(f"Product Link : {product_link}")
    #Exrtracting Product Price
    try:
        product_price =re.sub('[,₹Rs.]','',sc_soup2.find("span", attrs={'class': 'f_price'}).text)
        print(f"Product Price :₹{product_price}")
    except AttributeError:
        title_string = "NA"
        print("Product Price = ", title_string)

    #Extracting Product Review
    try:
        #rating = sc_soup2.find("div", attrs={'class': 'ratings'}).contents
        rating = sc_soup2.find("span", attrs={'class': 'val'}).text
        print(f"Overall Rating : {rating} ★")
    except AttributeError:
        rating="NA"
        print("Overall Rating = ", rating)   


usr=input('Please Enter Product Name : ')
#Step 1 is to clean the product name to make the product search easy
product_name=clean_prod_name(usr)
#Step 2 is to get product link for the searched product
sc_url=get_sc_link(product_name)
#Step 3 is creating Soup Object
sc_soup=sc_soup_object(sc_url)
#Step 4 is to find Product Link
product_link=get_product_link(sc_soup,product_name)
#Step 5 is to find Product Specs
product_specs(product_link)

