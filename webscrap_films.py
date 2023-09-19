#Scrapes IMDb for the top 250 films

import requests as rq
import csv
from bs4 import BeautifulSoup as bs


def extract_film_data(my_film):
    #get title
    title = my_film.find("h3", class_="ipc-title__text").text
    title = title.split(". ")[1]

    #get IMDb rating
    rating = my_film.find("span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating").text
    rating = rating.split()[0]

    #get year, length, content rating
    elements = my_film.find_all(class_="sc-b51a3d33-6 faLXbD cli-title-metadata-item")
    results = [title, rating, elements[0].text, elements[1].text, elements[2].text]
    return results

def main():
    #set up csv file for editing
    file = open('export_data_film.csv', 'w', newline='')
    writer = csv.writer(file)
    csvheaders = ['Title', 'IMDb Rating', 'Year', 'Length', 'Content Rating']
    writer.writerow(csvheaders)
    
    #set up request for html
    my_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    session = rq.Session()
    page = session.get(URL, headers=my_headers)
    soup = bs(page.content, "html.parser")
    
    #grab all film data
    films = soup.find_all(class_="sc-b51a3d33-0 hKhnaG cli-children")
    for film in films:
        film_data = extract_film_data(film)
        writer.writerow(film_data)
        for datum in film_data:
            print(datum)
        print()
    file.close()
    
main()

