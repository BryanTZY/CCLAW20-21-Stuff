import requests
from bs4 import BeautifulSoup
import os.path


def scrape():
    file_dir = "/Users/ruixin/Desktop/CCLAW" #change
    
    viet_root_url = "http://vbpl.vn/TW/Pages/vbpq-toanvan.aspx?ItemID="
    id_range = 5792 #change 
    
    for id_num in range(5792, id_range+1):
        url = viet_root_url + str(id_num)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser') 
        
        text = soup.find_all("div", class_="toanvancontent")
        
        #get name of document
        page_links = soup.find_all("div", class_="box-map")
        for i in page_links:
            file_name = (i.getText().strip().split('\n') [-1]).strip()
        file_name= file_name.replace('/','.') + '.vn'     
        
        #check for english version
        if soup.find('b', class_ = 'history').getText() == 'VB tiếng anh': #have english version
            vn_file_dir = file_dir + "/Viet"
            en_url = "http://vbpl.vn" + soup.find("div", class_="header").find('a').get('href')
            en_page = requests.get(en_url)
            soup = BeautifulSoup(en_page.text, 'html.parser') 
          
            en_text = soup.find_all("div", class_="fulltext")  #need to remove header?
                    
            links = soup.find_all("div", class_="box-map")
            for i in links:
                filename = (i.getText().strip().split('\n') [-1]).strip()
            filename= filename.replace('/','.') + '.en'   
            
            en_file_dir = file_dir + "/English"
            if not os.path.exists(en_file_dir): 
                os.makedirs(en_file_dir)
            
            with open (os.path.join(en_file_dir,filename), 'w') as f:
                for j in en_text:
                    f.write(j.getText().strip())        
                
                    
        else:
            vn_file_dir = file_dir + "/Viet-only"
            
         
        if not os.path.exists(vn_file_dir): 
            os.makedirs(vn_file_dir)
        with open (os.path.join(vn_file_dir,file_name), 'w') as file:
            for i in text:
                file.write(i.getText().strip()) 



scrape ()
        



    

