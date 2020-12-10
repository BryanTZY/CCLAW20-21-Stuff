from bs4 import BeautifulSoup
import re
import json
import requests 
import urllib.request

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def scrape_lawgazette_archive():
    url = "https://lawgazette.com.sg/archives"
    try:
        archive = requests.get(url, headers= headers)
    except:
        print("An error occurred.")

    soup = BeautifulSoup(archive.text, features="lxml")
    months = dict()

    for a in soup('a', 'issue-block'): #Finds all tags corresponding to a monthly archive
        months[a.get_text()] = a['href']

    for month_key, month_url in months.items():
        print(month_key, month_url)
        scrape_monthly_archive(months, month_key)

def scrape_monthly_archive(months, month_key):
    month_url = months[month_key]
    try:
        month_archive = requests.get(month_url, headers=headers)
    except: 
        print("Unable to excess monthly archive of ", month_key[:15])
    # print(month_archive.text)
    return

scrape_lawgazette_archive()





