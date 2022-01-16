#Webscraping and SQL Project
#By: Keeran Srikugan
#Date: December 27, 2021
from bs4 import BeautifulSoup
import requests
import tkinter as tk


def CreateURL(product):
    url = "https://www.amazon.ca/s?k={}&ref=nb_sb_noss_1"
    product = product.replace(' ', '+')
    return url.format(product)


def checkNewProduct():

    product = productText.get(1.0, "end-1c")

    if (bool(product) == False ):
        print("no product")
    else:
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36','Accept-Language': 'en-CA, en;q=0.5'})

        #This gets the url for the page that will be data scrapped
        search_url = CreateURL(product)

        #Here we begin scrapping by requesting access to the page, and then gathering the information we need
        webpage = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        item = results[0]

        #Here I check if the product name in all of the product boxes
        for i in range (0,len(results)-1):
            currentItem = results[i]
            itemName = currentItem.text
            if(product in itemName):
                
                #If I have found the product, I will send the link to the page so the user can ensure that it is the correct product
                item = results[i]
                print(item.text)
                atag = item.h2.a
                productURL = 'https://www.amazon.ca' + atag.get('href')
                print(productURL)
                break

                

                
                
                
                

            





root = tk.Tk()
root.geometry("700x400")
root.configure(bg = "#0E0066")
label1 = tk.Label(root, text = "Enter Product Name: ", bg = '#22316C', fg = 'white')
label1.place(x = 20, y = 10)


button1 = tk.Button(root, text = "Enter New Product", command = checkNewProduct)
button1.place(x = 300, y = 300)
productText = tk.Text(root, height = 1, width = 20)
productText.place(x = 200, y = 10)

label2 = tk.Label(root, text ="")
label2.place(x = 20, y = 50)





root.mainloop()






