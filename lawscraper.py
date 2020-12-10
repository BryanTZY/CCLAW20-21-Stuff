from bs4 import BeautifulSoup
import re
import json
import requests 
import urllib.request

url = "https://lawgazette.com.sg/archives"

try:
    archive = requests.get(url, headers= {'Accept': 'application/vnd.github.v3.text-match+json'})
    
except:
    print("An error occurred.")

# print(page.headers)

soup = BeautifulSoup(archive.text)
print(soup)

regex = re.compile('^issue-block-')
content_lis = soup.find_all('li', attrs={'class': regex})
print(content_lis)




