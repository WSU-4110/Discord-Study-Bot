from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
import time
import random
import json
from models import base_db_model

#This class uses both json and web scraping to get quotes from the internet and send to users
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

    # This method uses web scraping techniques to get quotes
    def get_cs_motivated(self):
        authors = []
        quotes = []
        url = 'https://fortrabbit.github.io/quotes/'
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.text, "html.parser")
        #try catch around web scraping in case html tags have been modified
        try:
            quote_text = soup.findAll('p', attrs={'class': 'type-l p-m'})
            quote_author = soup.findAll('div', attrs={'class': 'm-top-m'})
        except Exception as e:
            print(e)

        # For loops strip content of any white space and brackets
        for author_name in quote_author:
            author = author_name.text.strip().split('\n')[0]
            authors.append(author)

        for quote_content in quote_text:
            quote = quote_content.text.strip().split('\n')[0]
            quotes.append(quote)

        #Try catch in case number of quotes changes
        try:
            rand_num = random.randint(1, len(quotes))
        except Exception as e:
            print(e)

        return authors[rand_num] + ': ' + quotes[rand_num]

    # parses the user input from command and returns a string containing the user roles
    def parse_role(self, discord_role: str):
        role = ''
        for ele in discord_role.split(' '):
            if '<@&' in ele and '>' in ele:
                role += ele + ' '
        return role
