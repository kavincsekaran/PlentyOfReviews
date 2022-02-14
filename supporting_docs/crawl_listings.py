# homework 4
# goal: ranked retrieval, PageRank, crawling
# exports:
#   student - a populated and instantiated cs525.Student object
#   PageRankIndex - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents and providing a
#     ranked result set




# ########################################
# now, write some code
# ########################################
import bs4
from bs4 import BeautifulSoup   # you will want this for parsing html documents
import numpy as np 
import requests
import re
from selenium import webdriver

inverted_index = {}
listno = []
webaddress=[]
pageno=0


def scrape_listings(address,root):
    driver = webdriver.Chrome(executable_path="C:\\WPI\\InfoRet\\FinalProject\\chromedriver.exe")
    driver.get(address)
    html = driver.page_source
    soup = BeautifulSoup(html,"lxml")

    for i in soup.find_all('div', attrs={'itemprop':'itemListElement'}):
        for j in i.find_all('div'):
            output=j.get('id')
            if output != None and output[:7]=="listing":
                if output[9:] not in listno:
                    listno.append(output[9:])
                    for j in soup.find_all('div',attrs={'id' : output}):
                        for div in j:
                            webaddress.append(div.a['href'])
                            
    zz=0
    for x in soup.find_all('nav'):
        for y in x.find_all('li'):
            for z in y.find_all('a'):
                if zz==1:
                    temp=z['href']
                    navpath=temp[:-1]
                zz+=1
    root+=1
    
    return navpath


def navigate(qpath):
    root=0
    navpath=scrape_listings(qpath,root)
    root+=1
    while root<17:
        path='https://www.airbnb.com'+navpath+str(root)
        scrape_listings(path,root)
        root+=1
    return
def export(file):
    f = open(file, 'w')
    for i in range(len(listno)):
        x=listno[i]+', https://www.airbnb.com'+webaddress[i]+'\n'
        f.write(x)
    f.close()
        
    
basepath=('https://www.airbnb.com/s/Boston--MA/homes?refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&checkin=2018-04-06&checkout=2018-04-09&s_tag=uZ2vNwRa&ib=true')
#basepath=('https://www.airbnb.com/s/Boston--MA/homes?refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&checkin=2018-04-03&checkout=2018-04-31&s_tag=uZ2vNwRa&ib=true')
navigate(basepath)
export('C:\\WPI\\InfoRet\\FinalProject\\crawl3-22.txt')

print(listno)
print(len(listno))
