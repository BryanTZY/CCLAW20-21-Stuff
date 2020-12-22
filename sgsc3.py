from bs4 import BeautifulSoup
import requests 
import urllib.request
import math
import re
import dataclasses
import sys
import datetime
import os
from typing import List, Any 

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
case_list = []
root_url = "https://www.supremecourt.gov.sg/news/supreme-court-judgments/"
opts = [opt for opt in sys.argv[1:] if opt.startswith("--")]

def scrape_by_years(file_dir, start_year, end_year):

    year_url = root_url + "year/"
    
    for year in range(start_year, end_year + 1):
        url = year_url + str(year) + '/page/1'
        results = requests.get(url, headers=headers)
        soup = BeautifulSoup(results.text, "html5lib")

        #To find total number of cases, and cases per page, then divide to get total pages for this particular year
        total_cases = int(soup.find('div', class_="amount").get_text().strip(' \t\n')[:4])
        case_count = len(soup.find_all('div', class_="judgmentpage"))
        
        page_count = math.ceil(total_cases/case_count) #actual code line. Downloads all cases in the year
        # page_count = 3 #for testing purposes

        for i in range(1, page_count + 1): #Supcourt page numbering starts at 1
            scrape_numbered_page(year, i, file_dir)

    print("Total cases downloaded:", len(case_list), '\n')
    print("Cases downloaded:")
    for case in case_list:
        print(case)
    return

def scrape_numbered_page(year, pageno, file_dir): #scrape a page of judgments from a given year

    page_url = root_url + "year/" + str(year) + "/page/"
    root_pdf_url = "https://www.supremecourt.gov.sg" #use later to construct the judgment pdf link

    curr_url = page_url + str(pageno)
    results = requests.get(curr_url, headers=headers)
    soup = BeautifulSoup(results.text, "html5lib")
    
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

#display input format: python3 file_dir/xxxx.py 2016 2020 (--dir '/relative/dir')
USAGE = f"Usage: python {sys.argv[0]} [--help] | -- startyear endyear]" 

@dataclasses.dataclass
class Arguments: 
    start_year: int
    end_year: int = 0
        
def validate(args: List[str]):
    #check valid number of arguments 
    try:
        arguments = Arguments(args)
    except TypeError:
        raise SystemExit(USAGE)

    start_year= int(args[0])
    current_year: int = datetime.datetime.now().year

    #if optional 2nd argument passed in
    if len(args)>1 and args[1].isdigit():
        end_year=int(args[1])
        if end_year > current_year:
            print("Year cannot exceed", current_year)
            raise SystemExit()
        elif start_year > end_year:
            print("End year cannot be greater than start year.")
            raise SystemExit()
    else:
        end_year = start_year

    #check for invalid year args
    if start_year > current_year:
        print("Year cannot exceed", current_year)
        raise SystemExit()        
    
    return start_year, end_year

def get_dir(args):
    file_dir = os.getcwd()
    
    if "--dir" in opts:
        file_dir += args[-1]

    #check if given directory exists
    if os.path.isdir(file_dir):
        print("Chosen file directory:", file_dir)
        return file_dir
    else:
        print("You have entered an invalid directory. Please try again.")
        raise SystemExit()

def main() -> None:
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")] #year1, (year2), (/relative/directory)
    if not args:
        raise SystemExit(USAGE) 
    if args[0] == "--help":
        print(USAGE)
    else:
        start_year, end_year = validate(args)
        file_dir = get_dir(args)
        scrape_by_years (file_dir, start_year, end_year) #pass into scraper

if __name__ == "__main__":
    main()