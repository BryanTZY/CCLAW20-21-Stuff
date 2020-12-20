from bs4 import BeautifulSoup
import requests 
import urllib.request
import math
import re
import dataclasses
import sys
import datetime
from typing import List, Any 


headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
case_dict = dict()

def scrape_by_years(file_dir, start_year, end_year):

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/year/"
    
    for year in range(start_year, end_year + 1):
        url = root_url + str(year) + '/page/1'
        results = requests.get(url, headers=headers)
        soup = BeautifulSoup(results.text, "html5lib")

        #To find total number of cases, and cases per page, then divide to get total pages for this particular year
        total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
        case_count = len(soup.find_all('div', class_="judgmentpage"))
        
        # page_count = math.ceil(total_cases/case_count) #actual code line. Downloads all cases in the year
        page_count = 3 #for testing purposes

        for i in range(1, page_count + 1): #Supcourt page numbering starts at 1
            scrape_numbered_page(year, i, file_dir)
    casenames = [k for k, v in case_dict.items()]

    print("Total cases downloaded:", len(case_dict), '\n')
    print("Cases downloaded:")
    for case in casenames:
        print(case)
    return

def scrape_numbered_page(year, pageno, file_dir): #scrape a page of judgments from a given year

    root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/year/" + str(year) + "/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link

    curr_url = root_url + str(pageno)
    results = requests.get(curr_url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    page_case_dict = dict()
    
    judgment_divs = soup.find_all('div', class_="judgmentpage") 
    
    for i in judgment_divs:
        text = i.find('div', class_="text").find_all(text=True, recursive=False) #recursive=False so that bs4 does not search the divs nested within the judgment div
        caseref = i.find('ul', class_="decision").find('li').get_text() #neutral citation
        casename = re.sub('[\t\n\./]', '', text[1]).strip(' ') + ' ' + caseref
        pdf_link = i.find('a', class_ = "pdf-download")['href']
        case_dict[casename] = pdf_link # Keep a global copy of all case names and urls for reference purposes
        page_case_dict[casename] = pdf_link #Use this for downloading all PDFs on one page

    for k, v in page_case_dict.items():
        print("Now downloading", k, v, ' ...\n')
        pdf_url = root_pdf_url + v
        urllib.request.urlretrieve(pdf_url, file_dir + k + '.pdf') #If testing downloading of entire year (line 33), comment out this line.

    print("**Page", pageno, "done...**\n")
    return



#command-line

#display input format: python3 file_dir/xxxx.py -- 2016 2020
USAGE = f"Usage: python {sys.argv[0]} [--help] | -- startyear endyear]" 


@dataclasses.dataclass
class Arguments: 
    start_year: int
    end_year: int = 0
        
def validate(args: List[str]):
    
    start_year= int(args[0])
    current_year: int = datetime.datetime.now().year
    
    if len(args)>1 and args[1].isdigit():  #if optional 2nd argument passed in
        end_year=int(args[1])

    #check valid number of arguments 
    try:
        arguments = Arguments(args) 
    except TypeError:
        raise SystemExit(USAGE)
 
    #check year args are valid
    if start_year>current_year:
        print("Year cannot exceed", current_year)
        raise SystemExit()
    
    if len(args) > 1:
        if end_year>current_year:
            print("Year cannot exceed", current_year)
            raise SystemExit()
            
        elif start_year>end_year:
            print("End year cannot be greater than start year.")
            raise SystemExit()
    else:
        end_year = start_year
    
    return start_year, end_year
    

def main() -> None:
    args = sys.argv[1:]
    if not args:
        raise SystemExit(USAGE) 
    if args[0] == "--help":
        print(USAGE)
    else:
        start_year, end_year = validate(args)
        scrape_by_years (sys.argv[0], start_year, end_year) #pass into scraper


if __name__ == "__main__":
    main()
    
