from bs4 import BeautifulSoup
import re
import json
import requests 
import spacy
import math
import io
import random
import pdfplumber

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def sup_court_scraper():

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/page/"
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
        pdf_link = i.find('a', class_ = "pdf-download")
        case_dict[casename] = pdf_link['href']
        case_count += 1

    # page_count = math.ceil(total_cases/case_count)
    page_count = 20 #for testing purposes

    # for i in range(1, page_count + 1):
    #     scrape_numbered_page(i, case_dict)
    
    # print("Now printing case dictionary...")
    # for k, v in case_dict.items():
    #     print(k + ",", v,)
    # print()

    casenames = [k for k, v in case_dict.items()]
    casetext_dict = dict() #store lists of sentences of every judgment
    random_casename = random.choice(casenames)
    print(random_casename)
    pdf_scraper(case_dict[random_casename], casetext_dict)

    return

def pdf_scraper(pdf_url_fragment, casetext_dict):
    root_pdf_url = "https://www.supremecourt.gov.sg" 

    r = requests.get(root_pdf_url+pdf_url_fragment)
    f = io.BytesIO(r.content)

    case = pdfplumber.open(f)
    test_page = case.pages[4]
    print(test_page.width, test_page.height, '\n')
    if len(test_page.lines) > 0:
        line_dict = test_page.lines[0]
        height_from_bottom = line_dict['y1']
        cropped = test_page.crop((0, 120, test_page.width, test_page.height - height_from_bottom), relative=True )
        print(line_dict)
        print(cropped.extract_text())
    else:
        cropped = test_page.crop((0, 120, test_page.width, test_page.height - 120), relative=True)
        print(cropped.extract_text())
        print("UNCROPPED - NO CITATIONS")
    

    #Unresolved sentence issues
    #(1) Judgment numbers (2) ". [emphasis in original]" (3) O. 18 r. 7 (wrong??)
   
    # print(contents, '\n')
    # contents1 = contents.split('\n')
    # for i in contents1:
    #     print("**"+ i + "**")
    #     print()

    # contents2 = re.split(r'(?<=\w\.)\s', contents)
   

    return


def scrape_numbered_page(pageno, case_dict): #sub-function to scrape a page of judgments, given page number

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

    # for k, v in case_dict.items():
    #     print(k, v, '\n')
    print("Page", pageno, "done...")
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
