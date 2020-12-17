from bs4 import BeautifulSoup
import re
import sys
import requests 
import urllib.request
import math
import random
import wget

#Command-line code purely for scraping of supcourt judgments - no pdf parsing

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def sup_court_scraper(file_dir, start_year, end_year):

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
    pdf_root_url = "https://www.supremecourt.gov.sg"
    case_dict = dict()

    url = root_url + str(random.randint(1, 200)) #random page for testing purposes
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    
    #We find all divs ('boxes'), each div contains 1 judgment (case name, case citation, pdf object etc.)
    total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
    case_count = 0
    

    # page_count = math.ceil(total_cases/case_count)
    page_count = 2 #for testing purposes

    for i in range(1, page_count + 1): #Supcourt page numbering starts at 1
        scrape_numbered_page(i, case_dict, file_dir)
    
    print("Now printing full case dictionary...")
    for k, v in case_dict.items():
        print(k + ",", v,)
    print()

    casenames = [k for k, v in case_dict.items()]
    
    return

def scrape_numbered_page(pageno, case_dict, file_dir): #sub-function to scrape a page of judgments, given page number

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link

    url = root_url + str(pageno)
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    page_case_dict = dict()
    
    boxes = soup.find_all('div', class_="judgmentpage")

    
    for i in boxes:
        text = i.find('div', class_="text").find_all(text=True, recursive=False)
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n]', '', text[1]).strip(' ') + ' ' + caseref
        pdf_link = i.find('a', class_ = "pdf-download")
        case_dict[casename] = pdf_link['href'] # Keep a global copy of all case names and urls for reference purposes
        page_case_dict[casename] = pdf_link['href'] #Use this for downloading all PDFs on one page

    for k, v in page_case_dict.items():
        print("Now downloading", k, v, ' ...\n')
        pdf_url = root_pdf_url + v
        urllib.request.urlretrieve(pdf_url, file_dir + k + '.pdf')

    print("**Page", pageno, "done...**")
    return

sup_court_scraper('/mnt/c/Users/bryantan/Documents/School Stuff/SMU/Com Science/CCLAW20-21 Stuff/test/', 2020, 2020) #put your file save directory here
