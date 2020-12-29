from bs4 import BeautifulSoup
import requests 
import urllib.request
import math
import re
import sys
import os

def homepage():

    home_url = "http://vbpl.vn/TW/Pages/Home.aspx" #language: Vietnamese
    homepage = requests.get(home_url)
    soup = BeautifulSoup(homepage.text,"html5lib")
    # print(soup)

    #retrieve hrefs of each type of legislation
    category_ul = soup.find('ul', class_="category", id="loaiVB")
    category = category_ul.find_all('li')
    for i in category:
        link = i.find('a')['href']
        print(link)
    
    


homepage()