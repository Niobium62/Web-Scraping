#scraps data from all nonfiction books from toscrape.com

import requests as rq
import csv
from bs4 import BeautifulSoup as bs

CSV_HEADERS = ['Title', 'Rating', 'Price']
NUM_PAGES = 7
BASE_URL = "http://books.toscrape.com/catalogue/category/books/nonfiction_13/page-{}.html"

def extract_book_data(book):
    #get the title
    h3_tag = book.find('h3')
    a_tag = h3_tag.find('a')
    title_value = a_tag['title']

    #get the rating
    rating = book.select("p[class^=star]")
    rating = rating[0]
    rating_value = rating['class'][1] + " stars"

    #get the price
    price_value = book.find("p", class_="price_color").text
    my_list = [title_value, rating_value, price_value]
    
    return my_list

if __name__ == "__main__":
    #prepare csv for writing data
    file = open('export_data.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(CSV_HEADERS)

    #collect all data from each page
    for page_num in range (1, NUM_PAGES):
        url = BASE_URL.format(page_num)
        page = rq.get(url)

        #get the data from each book
        soup = bs(page.content, "html.parser")
        books = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        
        #write each book's data to csv
        for book in books:
            book_data = extract_book_data(book)
            writer.writerow(book_data)
            print("Title:\t" + book_data[0])
            print("Rating:\t" + book_data[1])
            print("Price:\t" + book_data[2])
            print()
    file.close()

    
