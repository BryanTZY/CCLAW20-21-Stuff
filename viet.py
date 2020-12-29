from bs4 import BeautifulSoup
import requests 
import urllib.request
import math
import re
import os, sys
from urllib.parse import urljoin, urlparse 

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

    scrape_by_category(category_links[5])

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
        title = box.find(class_="title").a
        doc_name = re.sub('[\t\n]', '', title.get_text()).strip(' ')
        doc_name = re.sub('/', '.', doc_name)
        print(doc_name)
        viet_link = title['href']
        link_list = [viet_link]
        doc_url = root_url + viet_link
        doc = requests.get(doc_url, headers=headers)
        docsoup = BeautifulSoup(doc.text, "html5lib")
        print_link = docsoup.find('div', class_="box-tab-vb").find('a', class_="clsatoanvan")['href']
        savePage(root_url + print_link, doc_name)

        eng_element = box.find('li', class_="en")
        eng_link = ''
        eng_bool = False
        if eng_element is not None:
            eng_bool = True
            eng_link = eng_element.a['href']
            link_list.append(eng_link)
        # print(link_list)

    # titles = soup.find('ul', class_="listLaw")(class_="title")
    # for title in titles:
    #     
    #     
    #     if 'anh' in first_tab.b.get_text(): #search for the English version tab
    #         eng_url = first_tab.a['href']
    #         print(eng_url)
    #     else:
    #         print("No english version found")
    print("Page", page_no, "complete\n")
        
def savePage(url, pagefilename='page'):
    def soupfindnSave(pagefolder, tag2find='img', inner='src'):
        """saves on specified `pagefolder` all tag2find objects"""
        if not os.path.exists(pagefolder): # create only once
            os.mkdir(pagefolder)
        for res in soup.findAll(tag2find):   # images, css, etc..
            try:         
                if not res.has_attr(inner): # check if inner tag (file object) exists
                    continue # may or may not exist
                filename = re.sub('\W+', '', os.path.basename(res[inner])) # clean special chars
                fileurl = urljoin(url, res.get(inner))
                filepath = os.path.join(pagefolder, filename)
                # rename html ref so can move html and folder of files anywhere
                res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                if not os.path.isfile(filepath): # was not downloaded
                    with open(filepath, 'wb') as file:
                        filebin = session.get(fileurl)
                        file.write(filebin.content)
            except Exception as exc:
                print(exc, file=sys.stderr)
        return soup
    
    session = requests.Session()
    #... whatever other requests config you need here
    response = session.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    pagefolder = pagefilename+'_files' # page contents
    soup = soupfindnSave(pagefolder, 'img', 'src')
    soup = soupfindnSave(pagefolder, 'link', 'href')
    soup = soupfindnSave(pagefolder, 'script', 'src')
    with open(pagefilename+'.html', 'wb') as file:
        file.write(soup.prettify('utf-8'))
    return soup



homepage()