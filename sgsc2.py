from bs4 import BeautifulSoup
import re
import sys
import requests 
import urllib.request
import math
import io
import random
import wget

#Command-line code purely for scraping of supcourt judgments - no pdf parsing

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    # file = open(filename + ".pdf", 'wb')
    # file.write(response.read())
    # file.close()
    str = response.read().decode('utf-8')
    pattern = re.compile('*.*')
    files = pattern.findall(str)
    # urllib.urlretrieve(dirpath + file, localfilelocation)

def sup_court_scraper(file_dir):

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
    pdf_root_url = "https://www.supremecourt.gov.sg"
    case_dict = dict()

    url = root_url + str(random.randint(1, 200)) #random page for testing purposes
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    
    boxes = soup.find_all('div', class_="judgmentpage")
    total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
    case_count = 0
    
    for i in boxes:
        text = i.find('div', class_="text").find_all(text=True, recursive=False)
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n]', '', text[1]).strip(' ') + ' ' + caseref
        casename = casename.replace('\\', ' ').replace('.', ' ')
        pdf_link = i.find('a', class_ = "pdf-download")
        case_dict[casename] = pdf_link['href']
        case_count += 1

    # page_count = math.ceil(total_cases/case_count)
    page_count = 1 #for testing purposes

    for i in range(1, page_count + 1):
        scrape_numbered_page(i, case_dict, file_dir)
    
    # print("Now printing case dictionary...")
    # for k, v in case_dict.items():
    #     print(k + ",", v,)
    # print()

    casenames = [k for k, v in case_dict.items()]
    casetext_dict = dict() #store lists of sentences of every judgment
    # random_casename = random.choice(casenames)
    # print(random_casename)

    return

def scrape_numbered_page(pageno, case_dict, file_dir): #sub-function to scrape a page of judgments, given page number

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link

    url = root_url + str(pageno)
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    
    boxes = soup.find_all('div', class_="judgmentpage")
    
    for i in boxes:
        text = i.find('div', class_="text").find_all(text=True, recursive=False)
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n]', '', text[1]).strip(' ') + ' ' + caseref
        pdf_link = i.find('a', class_ = "pdf-download")
        case_dict[casename] = pdf_link['href']

    for k, v in case_dict.items():
        print(k, v, '\n')
        pdf_url = root_pdf_url + v
        urllib.request.urlretrieve(pdf_url, file_dir + k + '.pdf')

    print("**Page", pageno, "done...**")
    return

sup_court_scraper('/mnt/c/Users/bryantan/Documents/School Stuff/SMU/Com Science/CCLAW20-21 Stuff/test/') #put your file save directory here
