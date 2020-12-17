from bs4 import BeautifulSoup
import re
import sys
import requests 
import urllib.request
import math

#Command-line code purely for scraping of supcourt judgments 

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
case_dict = dict()

def scrape_by_years(file_dir, start_year, end_year):

    if start_year > end_year or end_year > 2020:
        print("You have entered the wrong year")
        return

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/year/"
    
    for year in range(start_year, end_year + 1):
        url = root_url + str(year) + '/page/1'
        results = requests.get(url, headers=headers)
        soup = BeautifulSoup(results.text, "html5lib")

        #To find total number of cases, and cases per page, then divide to get total pages for this particular year
        total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
        judgment_divs = soup.find_all('div', class_="judgmentpage")
        case_count = len(judgment_divs)
        
        # page_count = math.ceil(total_cases/case_count) #actual code line
        page_count = 3 #for testing purposes

        for i in range(1, page_count + 1): #Supcourt page numbering starts at 1
            scrape_numbered_page(year, i, file_dir)
    casenames = [k for k, v in case_dict.items()]

    print("Total cases downloaded:", len(case_dict), '\n')
    print("Cases downloaded:")
    for case in casenames:
        print(case)
    return

def scrape_numbered_page(year, pageno, file_dir): #sub-function to scrape a page of judgments from a given year

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/year/" + str(year) + "/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link

    curr_url = root_url + str(pageno)
    results = requests.get(curr_url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    page_case_dict = dict()
    
    judgment_divs = soup.find_all('div', class_="judgmentpage")
    
    for i in judgment_divs:
        text = i.find('div', class_="text").find_all(text=True, recursive=False)
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n\./]', '', text[1]).strip(' ') + ' ' + caseref
        pdf_link = i.find('a', class_ = "pdf-download")['href']
        case_dict[casename] = pdf_link # Keep a global copy of all case names and urls for reference purposes
        page_case_dict[casename] = pdf_link #Use this for downloading all PDFs on one page

    for k, v in page_case_dict.items():
        print("Now downloading", k, v, ' ...\n')
        pdf_url = root_pdf_url + v
        urllib.request.urlretrieve(pdf_url, file_dir + k + '.pdf')

    print("**Page", pageno, "done...**\n")
    return

scrape_by_years('/mnt/c/Users/bryantan/Documents/School Stuff/SMU/Com Science/CCLAW20-21 Stuff/test/', 2016, 2016) #put your file save directory here