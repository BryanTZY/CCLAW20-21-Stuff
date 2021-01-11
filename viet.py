from bs4 import BeautifulSoup
import requests 
import urllib.request
from urllib.parse import urljoin, urlparse 
import os, sys, re, math

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
root_url = "http://vbpl.vn"
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")] #should be max only 1 arg, relative_dir
opts = [opt for opt in sys.argv[1:] if opt.startswith("--")]

#Remaining issue: documents with duplicate /'unnamed' name, overriding each other.
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

def start_scraping():

    home_url = "http://vbpl.vn/TW/Pages/Home.aspx" #language: Vietnamese
    homepage = requests.get(home_url, headers=headers)
    soup = BeautifulSoup(homepage.text,"html5lib")

    #retrieve hrefs of each type of legislation
    category_ul = soup.find('ul', class_="category", id="loaiVB")
    categories = category_ul.find_all('li')
    category_links = []

    for i in categories:
        category_element = i.find('a')
        category_name = re.sub('[\t\n]', '', category_element.get_text()).strip(' ')
        link = category_element['href'] #relative link
        category_links.append((category_name, link))
    
    # for k, v in category_links:
        # print("Now scraping documents under the category '", v[0], "'...")  
        # scrape_by_category(v[1])

    print("Now scraping legal documents of type '" +  category_links[6][0] + "'...") #for testing
    scrape_by_category(category_links[6][1]) #for testing

    print("Total parallel Vietnamese and English documents downloaded:", str(par_viet_count) + ",", par_eng_count)
    print("Total Vietnamese-only documents downloaded:", only_viet_count)

    return
    
def scrape_by_category(page_url_fragment):

    category_url = root_url + page_url_fragment
    category_page = requests.get(category_url, headers=headers)
    category_soup = BeautifulSoup(category_page.text, "html5lib")
    doc_count = int(category_soup.find('a', class_="selected").find('b').get_text())
    page_count = math.ceil(doc_count / 10) #seems to be 10 documents displayed per page 
    print("Total documents:", doc_count, "; total pages:", page_count)

    # for page_no in range(1, page_count + 1):
    #     scrape_page(category_url, page_no)

    scrape_page(category_url, 1) #for testing 

    return

def scrape_page(category_url, page_no):
    global par_viet_count #in order to change external variables within fn, necessary to refer to them as global first.
    global par_eng_count
    global only_viet_count

    page_url = category_url + "&Page=" + str(page_no)
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html5lib")
    boxes = soup.find('ul', class_="listLaw")(class_="item")

    #iterate through each document box, search for link to Vietnamese and English (if any), then download accordingly
    for box in boxes:
        if box.find(class_="source") is not None: #If there is a PDF button, skip this document.
            continue
        title_element = box.find(class_="title").a
        doc_name = re.sub('[\t\n]', '', title_element.get_text()).strip(' ')
        doc_name = re.sub('/', '.', doc_name)
        doc_url = root_url + title_element['href']
        doc = requests.get(doc_url, headers=headers)
        docsoup = BeautifulSoup(doc.text, "html5lib")
        viet_link = docsoup.find('a', class_="clsatoanvan")['href']
        
        #If there is a parallel English translation, download both
        eng_element = box.find('li', class_="en")
        try:
            eng_url = root_url + eng_element.a['href']
            engdoc = requests.get(eng_url, headers=headers)
            engsoup = BeautifulSoup(engdoc.text, "html5lib")
            eng_link = engsoup.find('b', class_= "print").parent.parent['href']
            print("Downloading both the Viet and English documents for", doc_name, "...")
            savePage(root_url + viet_link, doc_name, 'V') #download the parallel Viet
            savePage(root_url + eng_link, doc_name, 'E') #download the parallel English
            par_viet_count += 1
            par_eng_count += 1
        #if no English translation, then just download the Vietnamese document
        except:
            print("Downloading only the Vietnamese document for", doc_name, "...")
            savePage(root_url + viet_link, doc_name) #no eng translation, use default mode
            only_viet_count += 1
    
    print("Page", page_no, "complete...\n")
        
def savePage(url, pagefilename='page', mode='D'): #mode default D = vietnamese_only, V = parallel Viet, E = parallel Eng
    def soupfindnSave(pagefolder, tag2find='img', inner='src'):
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
    response = session.get(url)
    soup = BeautifulSoup(response.text, features="lxml")

    dir_dict = {'V': parallel_dir + '/' + pagefilename + '.vn', 'E': parallel_dir  + '/' + pagefilename + '.en', 'D': viet_dir + '/' + pagefilename + '.vn' }
    save_dir = dir_dict[mode]
    pagefolder = save_dir +' files' # page contents

    # soup = soupfindnSave(pagefolder, 'img', 'src') #No images observed so far. But if there are, then uncomment back this line.
    soup = soupfindnSave(pagefolder, 'link', 'href')
    soup = soupfindnSave(pagefolder, 'script', 'src')
    with open(save_dir + '.html', 'wb') as file:
        file.write(soup.prettify('utf-8')) #this should standardise to utf-8 as required
    return soup

start_scraping()