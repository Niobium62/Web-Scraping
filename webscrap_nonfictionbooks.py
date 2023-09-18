#This script will scrap data from all nonfiction books from toscrape.com.


import requests as rq
from bs4 import BeautifulSoup as bs

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

def main():
    for page_num in range (1,7):
        URL = "http://books.toscrape.com/catalogue/category/books/nonfiction_13/page-" + str(page_num) + ".html"
        page = rq.get(URL)
        
        soup = bs(page.content, "html.parser")
        books = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in books:
            book_data = extract_book_data(book)
            print("Title:\t" + book_data[0])
            print("Rating:\t" + book_data[1])
            print("Price:\t" + book_data[2])
            print()

main()

    
