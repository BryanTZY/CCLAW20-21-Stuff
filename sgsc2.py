from bs4 import BeautifulSoup
from datetime import datetime
import sys
import requests 
import urllib.request
import math
import re
import os

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/"
case_list = []
file_dir = ''
opts = [opt for opt in sys.argv[1:] if opt.startswith("--")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

#Update desired file_dir based on whether user used --rel (relative directory) option
if "--rel" in opts:
    curr_dir = os.getcwd()
    file_dir = curr_dir + args[-1]
else:
    file_dir = args[- 1]

if os.path.isdir(file_dir):
    print("Chosen file directory:", file_dir)
else:
    print("You have entered an invalid directory. Please try again.")
    sys.exit()

def scrape_by_years(start_year, end_year):
    if start_year > end_year or end_year > datetime.now().year: #temporary, should be removed after we code in years as args, and catch invalid args passed
        print("You have entered invalid year(s).")
        return

    year_url = root_url + "year/"
    
    for year in range(start_year, end_year + 1):
        url = year_url + str(year) + '/page/1'
        results = requests.get(url, headers=headers)
        soup = BeautifulSoup(results.text, "html5lib")

        #To find total number of cases, and cases per page, then divide to get total pages for this particular year
        total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
        case_count = len(soup.find_all('div', class_="judgmentpage"))
        
        # page_count = math.ceil(total_cases/case_count) #actual code line. Downloads all cases in the year
        page_count = 3 #for testing purposes

        for i in range(1, page_count + 1): #Supcourt page numbering starts at 1
            scrape_numbered_page(year, i)

    print("Cases downloaded:")
    for case in case_list:
        print(case)
    print("Total cases downloaded:", len(case_list), '\n')
    return

def scrape_numbered_page(year, pageno): #scrape a page of judgments from a given year

    page_url = root_url + "year/" + str(year) + "/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link

    curr_url = page_url + str(pageno)
    results = requests.get(curr_url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    page_case_dict = dict()
    
    judgment_divs = soup.find_all('div', class_="judgmentpage") 
    
    for i in judgment_divs:
        text = i.find('div', class_="text").find_all(text=True, recursive=False) #recursive=False so that bs4 does not search the divs nested within the judgment div
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n\./]', '', text[1]).strip(' ') + ' ' + caseref
        pdf_link = i.find('a', class_ = "pdf-download")['href']
        case_list.append(casename) # Keep a global copy of all case names for reference purposes
        print("Now downloading", casename, ' ...\n')
        pdf_url = root_pdf_url + pdf_link
        urllib.request.urlretrieve(pdf_url, file_dir + '/' + casename + '.pdf')

    print("**Page", pageno, "done...**\n")
    return

def parse_args(args): 
    #Based on args passed in by user, 
    # (1) determine if user wants single-year or multi-year download;
    # (2) catch invalid arguments (e.g. start_year > end_year)
    # (3) pass in the appropriate arguments to scrape_by_years.
    start_year = 0
    end_year = 0
    if args[0].isnumeric():
        start_year = int(args[0])
    else:
        print("You have entered an invalid start year. Now exiting program...")
        return

    if len(args) == 3:
        if args[1].isnumeric():
            end_year = int(args[1])
            print("Now scraping cases from", start_year, "to", end_year, "(both years inclusive)...")
            scrape_by_years(start_year, end_year) 
        else:
            print("You have entered an invalid end year.")
    elif len(args) == 2:
        #If user inputs only one year arg, implies user only wants to download from that year.
        #Pass in the same start and end year to download cases from just that year.
        print("Now scraping cases from", start_year, "only...")
        scrape_by_years(start_year, start_year) 
    else:
        print("You have entered too many arguments.")
        return

parse_args(args)