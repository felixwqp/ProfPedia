# -*- coding: utf-8 -*-


from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import re
import codecs
from string_function import *

def univNama(tag):
    return tag.name == u'td' and len(tag.attrs) == 0


if __name__ == "__main__":

    aiAreas = {"ai", "vision", "ml", "nlp", "web+ir"}
    systemsAreas = {"arch", "mobile", "security", "eda", "db", "mobile", "metrics", "se", "embedded", "hpc", "os", "pl","networks"}
    theoryAreas = {"theory", "crypto", "logic"}
    interdisciplinaryAreas = {"graphics", "hci", "robotics", "bio", "visualization", "ecom"}
    fieldDir = {'ai':aiAreas , 'system':systemsAreas, 'theory':theoryAreas, 'interdisciplinary': interdisciplinaryAreas}



    browser = webdriver.Chrome()
    browser.get('http://csrankings.org/')
    browser.find_element_by_id('all_areas_on').click()
    # time.sleep(5)
    # browser.find_element_by_id('ai').click()
    time.sleep(5)
    browser.find_element_by_id('Carnegie%20Mellon%20University-widget').click()
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    # file = open("html_CMU.txt", "w")
    # file.write(soup.prettify('latin-1'))
    # fileLink = open("CMU1.txt", "w")
    """the name and related link"""
    flag = False
    count = 0
    f = open('CMU1','r')
    f.close()
    for link in soup.find_all("a"):
        temp =  link.text, link.get("href")
        if temp[0] == 'Ariel D. Procaccia' or flag:
            flag = True
            tempStr = str(temp[0].encode('utf-8'))
            temp1 = str(temp[1].encode('utf-8'))
            if count%5 == 0:

                if(len(tempStr)<3):
                    continue
                f = open('profs/'+tempStr,'w')

            if count%5 == 1:
                f.write(temp1+'\n')
            if count % 5 == 2:
                f.write(temp1 + '\n')
            if count % 5 == 3 :
                f.write(temp1 + '\n')
            if count % 5 == 4:
                f.close()
            count+=1
    data = str()
    for link in soup.find_all(univNama):
        data += str(link.text.encode('utf-8')).replace('\n',' ')
    # print(data)

    data = re.sub(r'►','#',data)
    # data = re.sub(r'','#',data)
    data = re.sub(r'Faculty', '@',data)

    data = re.sub(r'[^A-Za-z0-9!@#\$%\^&\.\,\|\?\'\:\*\(\)\+ ]+', r' ', data)
    # data = re.sub(r'\'', r'\\'', data)

    data= re.sub(r'(\s+)',r' ', data)

    # print(data)
    data = data.replace('Carnegie', '# Carnegie')
    data = data.replace('#','\n#')



    name = re.findall(r'(?<=#)(.*)(?=@)',data)
    prof = re.findall(r'(?<=@)(.*)(?=)',data)

    for i in range(len(name)):
        if(len(name[i])<5):
            continue
        temp = name[i].strip()
        temp = temp.replace(' ', '_')
        f= open('universities/'+temp+'.txt' , 'w+')

        names = createFieldFiles(prof[i], fieldDir)

        for nameTemp in names:
            f.write(nameTemp+'\n')
        # f.write(prof[i])
        f.close()

    # data.replace('▼','#')
    # print(data)
    # for i in range(1,200):
    #     r'(?<=% of )(.*)(?= at )'