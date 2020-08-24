# How to Build a Web Scraper With Python [Step-by-Step Guide]
# Top 50 movies on IMDB
# Tutorial Source: https://hackernoon.com/how-to-build-a-web-scraper-with-python-step-by-step-guide-jxkp3yum

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
headers = {"Accept-Language": "en-US, en;q=0.5"}
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

#print(soup.prettify())

#initialize empty lists where you'll store your data
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')


for container in movie_div:

    name = container.h3.a.text
    titles.append(name)

    year = container.h3.find('span', class_='lister-item-year').text
    years.append(year)

    #time
    if container.find('span', class_='runtime')!= None:
        runtime = container.find('span', class_='runtime').text
    else:
        runtime = '_'
    time.append(str(runtime))

    #IMdb rating
    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)

    #metascore
    if container.find('span', class_='metascore')!= None:
        m_score = container.find('span', class_='metascore').text
    else:
        m_score = np.nan
    metascores.append(str(m_score))

    #here are two NV containers, grab both of them as they hold both the votes and the grosses
    nv = container.find_all('span', attrs={'name':'nv'})

    #filter nv for votes
    vote = nv[0].text
    votes.append(vote)

    # filter nv for gross
    if len(nv) > 1:
        grosses = nv[1].text
    else:
        grosses = '_'
    us_gross.append(grosses)




# print (titles )
# print (years )
# print (time )
# print (imdb_ratings )
# print (metascores )
# print (votes )
# print (us_gross )




movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': time,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMi11ions' : us_gross
})

movies['year'] =  movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] =  movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] =  movies['metascore'].astype(float)
movies['votes'] =  movies['votes'].str.replace(',','').astype(int)
movies['us_grossMi11ions'] =  movies['us_grossMi11ions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMi11ions'] =  pd.to_numeric(movies['us_grossMi11ions'], errors='coerce')


movies.to_csv('movies.csv')

