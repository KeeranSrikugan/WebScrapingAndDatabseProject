#Webscraping and SQL Project
#By: Keeran Srikugan
#Date: December 27, 2021
from bs4 import BeautifulSoup
import requests
import tkinter as tk
import psycopg2
import pandas as pd


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

        #Here I check if the product name in all of the product boxes avaiable, and if it is found then the link is outputted
        counter = 0
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
                productLinkText.insert(tk.END,productURL)
                label3["text"]= ""
                checkIfCorrectProduct()
                break
            counter = counter + 1

        if(counter >= len(results)-1):
            label3["text"] = "Incorrect Information"

#This function is simply used to call the 2 buttons into the frame
def checkIfCorrectProduct():
    button2.place(x = 200, y = 250)
    button3.place(x = 400, y = 250)

    
    
#This function runs if the product 
def incorrectProduct():
    button2.place(x = 5000, y = 5000)
    button3.place(x = 5000, y = 5000)
    
    productText.delete(1.0,"end")
    productLinkText.delete(1.0,"end")

    


def addToDatabase():
    
    #Here I forget the buttons since they are not needed anymore.
    button2.pack()
    button3.pack()
    button1.pack()
    button2.pack_forget()
    button3.pack_forget()
    button1.pack_forget()


    
    
    

    #Below, I will be collecting all the information needed for the databse
    productLink = productLinkText.get(1.0, "end-1c")
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36','Accept-Language': 'en-CA, en;q=0.5'})
    webpage = requests.get(productLink, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")

    #This is where I get the price of the product
    prices = soup.find_all('div', {'id': 'apex_desktop'})
    price = prices[0].span.span.text

    
    print(price)


    #This is where I get the manufacturer
    
    

    #This is where I get the name of the product
    product = productText.get(1.0, "end-1c")

    #This is where I get the rating of the product:
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""
    print(rating.split()[0])

    #This is where I get the weblink
    label4 = tk.Label(root, text = "PgAdmin Password: ", bg = '#22316C', fg = 'white')
    label4.place(x = 20, y = 150)

    #How to get the seller

    databasePassword = tk.Text(root, height = 2, width = 45)
    databasePassword.place(x = 200, y = 150)

    

    

    
                
                
                

#Here is where the UI is created            
root = tk.Tk()
root.geometry("700x400")
root.configure(bg = "#0E0066")

label1 = tk.Label(root, text = "Enter Product Name: ", bg = '#22316C', fg = 'white')
label1.place(x = 20, y = 10)

label2 = tk.Label(root, text = "Product Webpage: ", bg = '#22316C', fg = 'white')
label2.place(x = 20, y = 75)

label3 = tk.Label(root, text = "", bg = '#0E0066', fg = '#E154FA')
label3.place(x = 295, y = 135)


button1 = tk.Button(root, text = "Enter New Product", command = checkNewProduct)
button1.place(x = 300, y = 170)

productText = tk.Text(root, height = 1, width = 20)
productText.place(x = 200, y = 10)


productLinkText = tk.Text(root, height = 2, width = 45)
productLinkText.place(x = 200, y = 75)

button2 = tk.Button(root, text = "Correct Product", command = addToDatabase)
button2.place(x = 5000, y = 5000)

button3 = tk.Button(root, text = "Incorrect Product", command = incorrectProduct)
button3.place(x = 5000, y = 5000)





root.mainloop()






