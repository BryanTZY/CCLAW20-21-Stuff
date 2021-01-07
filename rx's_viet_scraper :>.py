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
        with open (os.path.join(vn_file_dir,filename), 'w') as file:
            for i in text:
                file.write(i.getText().strip()) 


#command-line

#display input format: python3 viet.py (--dir /relative/dir)
USAGE = f"Usage: python {sys.argv[0]} [--help] | -- ]" 


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


        



    
    
    
    

#directory (make 3 folders)
scrape()
