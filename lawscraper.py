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
    month_keys = [] #use only when need to assess specific year / for testing

    for a in soup('a', 'issue-block'): #Finds all tags corresponding to a monthly archive
        archive_list_words = a.get_text().split(' ')
        archive_name = archive_list_words[1] + ' ' + archive_list_words[2]
        months[archive_name] = a['href']
        month_keys.append(archive_name)
    
    #Now, scrape the articles by month
    scrape_monthly_archive(month_keys[0], months[month_keys[0]]) #for testing purposes
    # for month_key, month_url in months.items():
        # print(month_key, month_url)
        # scrape_monthly_archive(month_key, month_url)

def scrape_monthly_archive(month_key, month_url):
    print("**Now scraping: ", month_key, "**")
    
    try:
        month_archive = requests.get(month_url, headers=headers)
    except: 
        print("Unable to excess monthly archive of ", month_key)

    soup = BeautifulSoup(month_archive.text, features = "lxml")
    result_list = soup.find_all('h3','a', class_="entry-title mkdf-post-title")
    articles = dict()
    article_list = []

    for x in result_list:
        article_name = x.get_text().strip()
        if len(article_name) > 7: #arbitrary small value, to remove stray links
            articles[article_name] = x.a['href']
            article_list.append(article_name)

    for article_name, article_url in articles.items():
        print(article_name + ',', article_url)
    print()

    scrape_article(article_list[10], articles[article_list[10]])

    return

def scrape_article(article_name, article_url):
    print("Now working on: '", article_name, "'")
    try:
        article_page = requests.get(article_url, headers=headers)
    except: 
        print("Unable to access the article, '", article_name, "'")
        return
    
    soup = BeautifulSoup(article_page.text, features = 'lxml')
    result = soup.find('div', class_="mkdf-post-text-main")
    result_soup =  result.find_all('p')

    para_list = []
    for p in result_soup:
        para_list.append(p.get_text())

    for para in para_list:
        print(para)
        print()

    return

scrape_lawgazette_archive()





