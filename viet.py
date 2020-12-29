from bs4 import BeautifulSoup
import requests 
import urllib.request
import math
import re
import sys
import os

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
root_url = "http://vbpl.vn"

def homepage():

    home_url = "http://vbpl.vn/TW/Pages/Home.aspx" #language: Vietnamese
    homepage = requests.get(home_url, headers=headers)
    soup = BeautifulSoup(homepage.text,"html5lib")

    #retrieve hrefs of each type of legislation
    category_ul = soup.find('ul', class_="category", id="loaiVB")
    category = category_ul.find_all('li')
    category_links = []

    for i in category:
        link = i.find('a')['href'] #relative link
        category_links.append(link)
        # print(link)
    
    # for i in category_links:
    #     scrape_by_category(i)

    scrape_by_category(category_links[1])

    return
    
def scrape_by_category(page_url_fragment):

    category_url = root_url + page_url_fragment
    category_page = requests.get(category_url, headers=headers)
    category_soup = BeautifulSoup(category_page.text, "html5lib")

    count_element = category_soup.find('a', class_="selected")
    doc_count = int(count_element.find('b').get_text())

    #seems to be 10 documents displayed per page 
    page_count = math.ceil(doc_count / 10)
    print(page_count)

    # for page_no in range(1, page_count + 1):
    #     scrape_page(category_url, page_no)

    scrape_page(category_url, 1)

    return

def scrape_page(category_url, page_no):
    page_url = category_url + "&Page=" + str(page_no)
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html5lib")
    boxes = soup.find('ul', class_="listLaw")(class_="item")

    #iterate through each document box and search for the link to Vietnamese and English (if any)
    for box in boxes:
        doc_link = box.find(class_="title").a['href']
        print(doc_link)
        doc_url = root_url + doc_link
        eng_element = box.find('li', class_="en")
        eng_link = ''
        if eng_element is not None:
            print("Link to English version found")
            eng_link = eng_element.a['href']

    # titles = soup.find('ul', class_="listLaw")(class_="title")
    # for title in titles:
    #     doc_link = title.find('a')['href']
    #     doc_url = root_url + doc_link
    #     eng = title.find()
    #     doc = requests.get(doc_url, headers=headers)
    #     docsoup = BeautifulSoup(doc.text, "html5lib")
    #     first_tab = docsoup.find('div', class_="box-tab-vb").find('div', class_="header").ul.li
    #     if 'anh' in first_tab.b.get_text(): #search for the English version tab
    #         eng_url = first_tab.a['href']
    #         print(eng_url)
    #     else:
    #         print("No english version found")
        




homepage()