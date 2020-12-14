from bs4 import BeautifulSoup
import re
import json
import requests 
import spacy
import math
# import docx
import random #for testing purposes

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def scrape_nsw_caselaw():

    url = "https://www.caselaw.nsw.gov.au/browse?display=all"
    # url = root_url + '1' #iteratively visit each page containing 200 results

    casepage = requests.get(url, headers= headers)

    soup = BeautifulSoup(casepage.text, features="lxml")
    total_count_soup = soup.find('small', class_="pageinfo hidden-xs")
    start_num = float(total_count_soup.find('span', class_="start").get_text())
    end_num = float(soup.find('span', class_="end").get_text())
    total_num = float(soup.find('span', class_="total").get_text())
    total_pages = total_num / (end_num - start_num + 1) #total number of pages of cases in database
    # print(math.ceil(total_pages)) 
    case_dict = dict()

    result = soup.find_all('h4')
    for x in result:
        case = x.find('a')
        case_dict[case.get_text()] = case['href']
    casenames = [k for k, v in case_dict.items()]

    # for k, v in case_dict.items():
    #     print(k, v)
    random_casename = random.choice(casenames)
    scrape_case(random_casename, case_dict[random_casename])


def scrape_case(casename, caseurl):
    url = "https://www.caselaw.nsw.gov.au" + caseurl + '/export.docx'
    casepage = requests.get(url, headers=headers)
    
    
    

    
    
    # month_keys = [k for k, v in months.items()]
    # print("Months found:", month_keys)

    # #**Test scraping with a random month**
    # random_month = random.choice(month_keys) 
    # print("\nNow scraping the'" + random_month + "' archive.")
    # cont_var = input("Continue? Y/N")
    # if cont_var.lower() == "y":
    #     scrape_monthly_archive(random_month, months[random_month]) 
    # else:
    #     print("End.")
    #     return

scrape_nsw_caselaw()