#Scraps all CPU prices from Canada Computers

import requests as rq
import csv
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

SCROLL_PAUSE_TIME = 0.85
CSV_HEADERS = ['Product', 'Current Price']
URL = "https://www.canadacomputers.com/index.php?cPath=4"

def get_all_contents(driver):
    #get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        #scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        #if current height has not changed after SCROLL_PAUSE_TIME seconds,
        current_height = driver.execute_script("return document.body.scrollHeight")
        if current_height == last_height:
            #return html contents of the entire page
            contents = driver.page_source
            driver.close()
            print("...")
            print("Writing contents to csv, please wait...")
            print("...")
            print()
            return contents
        #keep track of the last height
        last_height = current_height

def write_data(products, prices):

    #prepare csv for writing data
    file = open('export_data_cpu.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(CSV_HEADERS)

    #for each product,
    for i in range(0, len(prices)):
        #write the product name and price to csv
        writer.writerow([products[i].text, prices[i].text])
        print("Product: " + products[i].text)
        print("Price: " + prices[i].text)
        print()
    file.close()

if __name__ == "__main__":
    #open url
    driver = webdriver.Chrome()
    driver.get(URL)

    #scroll down all the way
    contents = get_all_contents(driver)

    #get html contents of browser
    soup = bs(contents, 'html.parser')

    #find all products
    products = soup.findAll("a", class_='text-dark text-truncate_3') 

    #find all prices
    prices = soup.findAll("span", class_=lambda x: x and x.endswith('d-block mb-0 pq-hdr-product_price line-height'))

    #write the products and their prices to a csv
    write_data(products, prices)