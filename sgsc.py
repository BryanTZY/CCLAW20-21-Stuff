from bs4 import BeautifulSoup
import re
import json
import requests 
import spacy
import math
import io

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def sup_court_scraper():

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link
    case_dict = dict()

    url = root_url + '23'
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    
    boxes = soup.find_all('div', class_="judgmentpage")
    total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
    case_count = 0
    
    for i in boxes:
        text = i.find('div', class_="text").find_all(text=True, recursive=False)
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n]', '', text[1]).strip(' ') + ' ' + caseref
        pdf_link = i.find('a', class_ = "pdf-download")
        case_dict[casename] = pdf_link['href']
        case_count += 1

    # page_count = math.ceil(total_cases/case_count)
    page_count = 20 #for testing purposes

    # for i in range(1, page_count):
    #     scrape_numbered_page(i, case_dict)
    
    for k, v in case_dict.items():
        print(k, v, '\n')

    return

def scrape_numbered_page(pageno, case_dict): #pageno should be int

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link

    url = root_url + str(pageno)
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    
    boxes = soup.find_all('div', class_="judgmentpage")
    total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
    
    for i in boxes:
        text = i.find('div', class_="text").find_all(text=True, recursive=False)
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n]', '', text[1]).strip(' ') + ' ' + caseref
        pdf_link = i.find('a', class_ = "pdf-download")
        case_dict[casename] = pdf_link['href']

    for k, v in case_dict.items():
        print(k, v, '\n')

    return

def sup_court_pinpoint_scraper():

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link
    case_dict = dict()

    url = root_url + '23'
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    
    boxes = soup.find_all('div', class_="judgmentpage")
    total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
    print(total_cases)
    case_count = 0
    
    for i in boxes:
        text = i.find('div', class_="text").find_all(text=True, recursive=False)
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n]', '', text[1]).strip(' ') + ' ' + caseref
        pdf_link = i.find('div', class_="download")
        case_dict[casename] = pdf_link.a['href']
        case_count += 1

    for k, v in case_dict.items():
        print(k, v, '\n')
    page_count = math.ceil(total_cases/case_count) #FYI

    return

sup_court_scraper()
