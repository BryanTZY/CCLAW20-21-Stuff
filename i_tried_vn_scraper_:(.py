from bs4 import BeautifulSoup
import requests
import os, sys, re, math

# sorry, I had to use your's, Bryan :'( idk how to create directories or...what this is
headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
root_url = "http://vbpl.vn"
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")] #should be max only 1 arg, relative_dir
opts = [opt for opt in sys.argv[1:] if opt.startswith("--")]

def get_dir(args):
    file_dir = os.getcwd()
    if "--dir" in opts:
        file_dir += args[0]

    #check if given directory exists
    if os.path.isdir(file_dir):
        print("Chosen file directory:", file_dir)
        return file_dir
    else:
        print("You have entered an invalid directory. Please try again.")
        raise SystemExit()

def make_dirs(dir_list):
    for i in dir_list:
        if not os.path.exists(i):
            os.mkdir(i)
    return

file_dir = get_dir(args)
parallel_dir = file_dir + '/Parallel'
viet_dir = file_dir + '/Vietnamese_Only'
make_dirs([parallel_dir, viet_dir])
par_eng_count, par_viet_count, only_viet_count =  0, 0, 0

def scrape():
    source = requests.get('http://vbpl.vn/TW/Pages/Home.aspx').text
    soup = BeautifulSoup(source, 'html5lib')
    
    # by promulgator
    categories = soup.find('ul', class_='category', id = "capCQ")
    category = categories.find_all('li')
    links = []
    for i in category:
        cat_src = i.find('a')['href']
        cat_id = cat_src.split('/')[3]
        cat_id = cat_id.split('?')[1]
        cat_link = f'http://vbpl.vn/TW/Pages/vanbanTA.aspx?{cat_id}'
        links.append(cat_link)

    # by type of documents
    categories = soup.find('ul', class_='category', id = "loaiVB")
    category = categories.find_all('li')
    doc_links = []
    for i in category:
        cat_src = i.find('a')['href']
        cat_id = cat_src.split('/')[3]
        cat_id = cat_id.split('?')[1]
        cat_link = f'http://vbpl.vn/TW/Pages/vanbanTA.aspx?{cat_id}'
        doc_links.append(cat_link)

    # check if only vn or also got en
    en = soup.find('b', class_='history')
    if en.text == 'VB tiếng anh':
        print('VB tiếng anh') # just to check but im getting an error
scrape()

