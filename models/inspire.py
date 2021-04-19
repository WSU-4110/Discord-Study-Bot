from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
import time
import random
import json
from models import base_db_model


class Inspire(base_db_model.BaseDBModel):
    def __init__(self):
        pass
    def get_cs_satire(self):
        url = 'http://quotes.stormconsultancy.co.uk/random.json'
        r = requests.get(url)
        quote = r.json()
        return quote['author'] + ':' + quote['quote']

    def get_inspiration(self):
        url = 'https://zenquotes.io/api/random'
        r = requests.get(url)
        quote = r.json()
        return quote[0]['a'] + ': ' + quote[0]['q']

    def get_cs_motivated(self):
        rand_num = random.randint(1, 189)
        authors = []
        quotes = []
        url = 'https://fortrabbit.github.io/quotes/'
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.text, "html.parser")
        quote_text = soup.findAll('p', attrs={'class': 'type-l p-m'})
        quote_author = soup.findAll('div', attrs={'class': 'm-top-m'})

        for q in quote_author:
            author = q.text.strip().split('\n')[0]
            authors.append(author)

        for i in quote_text:
            quote = i.text.strip().split('\n')[0]
            quotes.append(quote)

        return authors[rand_num] + ': ' + quotes[rand_num]