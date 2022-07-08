

# scrape.py
# scrapes earning call data from Seeking Alpha

import requests
import time
from bs4 import BeautifulSoup
import os
import io
mainfolder=os.getcwd()
D2=mainfolder+"/Data"
#print(os.path.isdir(D2))
if(os.path.isdir(D2)==False):
    os.mkdir(D2)
os.chdir(D2)
# def get_date(c):
#     end = c.find('|')
#     return c[0:end-1]

# def get_ticker(c):
#     beg = c.find('(')
#     end = c.find(')')
#     return c[beg+1:end]



for i in range(1,200): #choose what pages of earnings to scrape
    #process_list_page(i)
    origin_page = "https://seekingalpha.com/earnings/earnings-call-transcripts" + "/" + str(i)
    print("trying to scrap " + origin_page)
    page = requests.get(origin_page)
    page_html = page.text
    #print(page_html)
    soup = BeautifulSoup(page_html, 'html.parser')
    alist = soup.find_all("li",{'class':'list-group-item article'})
    # text=alist[0].get_text()
    # print(text)
    for i in range(0,len(alist)):
        url_ending = alist[i].find_all("a")[0].attrs['href']
        url = "https://seekingalpha.com" + url_ending
        #print( )
        #print(url)
        #print( )
        #grab_page(url)
        print("attempting to grab page: " + url)
        page = requests.get(url)
        page_html = page.text
        soup = BeautifulSoup(page_html, 'html.parser')
        wording=url.split("/")
        l=len(wording)
        #meta = soup.find("div",{'class':'sa-art article-width'})
        content = soup.find(id="a-body")
    
        if type(content) == "NoneType" or str(content)=="None":
            print("skipping this link, no content here")
            continue
        else:
            # print(type(content))
            # #print(content)
            # text = content.text
            #mtext = meta.text
    
            filename = wording[l-1]
            file = open(filename.lower() + ".html", 'w',encoding="utf-8")
            file.write(str(content))
            file.close
            print(filename.lower()+ " sucessfully saved")
        time.sleep(.5)