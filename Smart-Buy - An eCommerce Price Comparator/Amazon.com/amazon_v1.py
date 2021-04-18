#Amazon Code
import re
import requests
from bs4 import BeautifulSoup
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

userProductName=input('Please enter your product name : ')

def fetch_URL(pName):
    pName1=pName.replace(' ','-')
    pName2=pName.replace(' ','+')
    amazon_url=f'https://www.amazon.in/{pName1}/s?k={pName2}'
    #print(amazon_url)
    webpage_request=requests.get(amazon_url,headers=HEADERS)
    soup_object1=BeautifulSoup(webpage_request.content,'html5lib')
    return soup_object1

if __name__ == '__main__':
    soup_object1=fetch_URL(userProductName)
    productFinalUrl=''
    flag=0
    for pName in soup_object1.find_all('span',attrs={'class':(re.compile('a-text-normal$'))}):
        if userProductName.lower() in  pName.string.lower():
            print(f'Product Found is : {pName.string}')
            parent_tag=pName.parent
            href=parent_tag.get('href')
            productFinalUrl=f'https://www.amazon.in{href}'
            flag=1
        if flag==1:
            break
    r=requests.get(productFinalUrl,headers=HEADERS)
    soup_object2=BeautifulSoup(r.content,'html5lib')
  

#Exrtracting Product Price
    try:
        product_price = soup_object2.find('span',attrs={'id': (re.compile('price$'))}).get_text(strip=True)
        print("Price of Product is : ",end='')
        print(product_price.replace(',',''))          
    except AttributeError:
        title_string = "NA"
        print("Product Price = ", title_string)

    #Exrtracting Product Availability
    try:
        avail=soup_object2.find('div',attrs={'id':'availability'}).span.get_text(strip=True)
        print("Product Available/Out of Stock : ",end='')
        print(avail)
    except AttributeError:
        available = "NA"
        print("Availability = ",available)

    #Extracting Product Review
    try:
        rating = soup_object2.find("span", attrs={'class': 'a-icon-alt'}).string
        print("Overall Rating of the product is : ",end='')
        print(rating)
    except AttributeError:
        rating="NA"
        print("Overall rating = ", rating)

