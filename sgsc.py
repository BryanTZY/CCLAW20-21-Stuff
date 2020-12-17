from bs4 import BeautifulSoup
import re
# import json
import requests 

import math
import io
import random
import pdfplumber
import spacy


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
    total_pages = len(case.pages)

    judgment_text = ''

    #Following method works for post-2016 judgments only.
    for i in range(0, 5):
        current_page = case.pages[i]
        text = ''
        if len(current_page.lines) > 0 and current_page.lines[0]['y1'] < current_page.width/2:
            height_from_bottom = current_page.lines[0]['y1']
            cropped = current_page.crop((0, 120, current_page.width, current_page.height - height_from_bottom), relative=True )
            text = cropped.extract_text()
            # print("FOOTNOTED \n")
        else:
            cropped = current_page.crop((0, 120, current_page.width, current_page.height - 120), relative=True)
            text = cropped.extract_text()
            # print("NO FOOTNOTES \n")
        judgment_text += text
        
    index = re.search(r'(?<=[)JRAC]):', judgment_text).start()
    print(judgment_text[index:]) #Print the judgment starting at the colon after the name of the judge delivering judgment

   #Possible issue - some judges use O. xx r. xx in quoting ROC

    # print(contents, '\n')
    # contents1 = contents.split('\n')
    # for i in contents1:
    #     print("**"+ i + "**")

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

sup_court_scraper()
