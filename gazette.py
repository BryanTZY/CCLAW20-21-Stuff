from bs4 import BeautifulSoup
import re
import json
import requests 
import spacy
import string
import random #for testing purposes
#note:
#on wsl, to run - "python3 xxxxx.py" --> must be python3!

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def scrape_lawgazette_archive():
    url = "https://lawgazette.com.sg/archives"

    try:
        archive = requests.get(url, headers= headers)
    except:
        print("Unable to access archive.")

    soup = BeautifulSoup(archive.text, features="lxml")
    months = dict()

    for a in soup('a', 'issue-block'): #Finds all tags corresponding to a monthly archive
        archive_list_words = a.get_text().split(' ')
        archive_name = archive_list_words[1] + ' ' + archive_list_words[2]
        months[archive_name] = a['href']
    
    month_keys = [k for k, v in months.items()]
    print("Months found:", month_keys)

    #**Test scraping with a random month**
    random_month = random.choice(month_keys) 
    print("\nNow scraping the'" + random_month + "' archive.")
    cont_var = input("Continue? Y/N")
    if cont_var.lower() == "y":
        scrape_monthly_archive(random_month, months[random_month]) 
    else:
        print("End.")
        return

    #Now, scrape the articles by month
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

    for x in result_list:
        article_name = x.get_text().strip()
        if len(article_name) > 7: #arbitrary small value, to remove stray links
            articles[article_name] = x.a['href']
    article_list = [k for k,v in articles.items()]
    print("Articles found:", article_list)

    #Continue test with a random article
    random_article = random.choice(article_list)
    scrape_article(random_article, articles[random_article])
    
    # for i in article_list:
    #     scrape_article(i, articles[i])

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
        sentences = []
        # print(para)
        sentences = re.split(r'(?<=\w\.)\s', para) #for each para, make a list of its sentences.
        # print(sentences)
        tokenize(sentences[0]) #sample a sentence in the paragraph for tokenization.
        
    print("Finished sentence sampling in the article, '" + article_name + "'" )
    return

def tokenize(para):
    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(para)
    print(list(doc))
    # for token in doc:
    #     print(token)
    print()

    return

scrape_lawgazette_archive()





