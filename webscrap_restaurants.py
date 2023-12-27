#grabs data from all Yelp restaurants near North York, ON, Canada

import requests as rq
import csv
from bs4 import BeautifulSoup as bs
import re

CSV_HEADERS = ['Restaurant Name', 'Rating', 'Tags', 'Price Range']
BASE_URL = "https://www.yelp.com/search?find_desc=&find_loc=North+York%2C+Toronto%2C+Ontario&start={}"
USER_AGENT = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
NUM = 0

def extract_data(restaurant):

    #get name, rating, and tags
    name = restaurant.find(class_="css-19v1rkv").text
    rating = restaurant.find(class_="css-gutk1c").text
    tags = restaurant.find_all(class_="css-11bijt4")
    for k in range (0, len(tags)):
        tags[k] = tags[k].text

    #get price range, if it exists
    try:
        price_range = restaurant.find(class_=lambda x: x and x.startswith('priceRange__')).text
    except:
        price_range = "Not specified"

    #return data
    return [name, rating, tags, price_range]

def get_num_pages():
    #request url
    url = BASE_URL.format(0)
    page = rq.get(url, headers=USER_AGENT)
    soup = bs(page.content, "html.parser")
    #pagination_info = soup.find(class_='pagination__09f24__VRjN4 css-1dhksiy')
    #find the element that contains the info for pagination
    pagination_info = soup.find_all('div', class_=lambda value: value and value.startswith("pagination__09f24"))
    print (pagination_info is None)
    #find the number of pages within that element
    pagination_info = pagination_info[0].find(class_="css-1aq64zd").text
    num_pages = pagination_info.split(" ")
    num_pages = int(num_pages[len(num_pages)-1])
    return num_pages

if __name__ == "__main__":

    #prepare csv for writing
    file = open('export_data_restaurants.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(CSV_HEADERS)

    num_pages = get_num_pages()
    for i in range(0, num_pages):

        #get content from each page
        url = BASE_URL.format(i*10)
        page = rq.get(url, headers=USER_AGENT)
        soup = bs(page.content, "html.parser")

        #get all restaurants listed on each page
        restaurants = soup.find_all(class_="css-ady4rt")

        #go through each restaurant, excluding the sponsored ones
        #the first eight on each page are sponsored. skip those
        for j in range (8, len(restaurants)-1):
            NUM = NUM + 1
            restaurant = restaurants[j]
            #extract data from each restaurant including name, rating, etc
            restaurant_data = extract_data(restaurant)
            #write data to csv
            writer.writerow(restaurant_data)
            #print data
            print(str(NUM) +")")
            for l in range(0, len(restaurant_data)):
                print(restaurant_data[l])
            print()
    file.close()
            
        
