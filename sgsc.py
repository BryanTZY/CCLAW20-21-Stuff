from bs4 import BeautifulSoup
import re
import json
import requests 
import spacy
import math
import random #for testing purposes

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def sup_court_scraper():

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
    url = root_url + '1'
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    
    case_dict = dict()
    boxes = soup.find_all('div', class_="judgmentpage")
    
    for i in boxes:
        text = i.find('div', class_="text").find_all(text=True, recursive=False)
        casename = re.sub('[\t\n]', '', text[1]).strip(' ')
        pdf_link = i.find('div', class_="download")
        # print(pdf_link.a['href'])
        case_dict[casename] = pdf_link.a['href']

    for k, v in case_dict.items():
        print(k, v, '\n')


    return

sup_court_scraper()