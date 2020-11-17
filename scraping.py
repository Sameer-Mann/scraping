from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import requests
import os
import json

data = json.load(open("data.json","r"))
saveDir = data["saveDir"]
driver = webdriver.Chrome()
try:
    for name in data['names']:
        os.chdir(saveDir)
        if name not in os.listdir():
            os.mkdir(name)
            os.chdir(name)
        driver.get(data['names'][name]['url'])
        sleep(2)
        elm = driver.find_element_by_css_selector("div.listing-chapters_wrap>ul.main>li.wp-manga-chapter>a")
        chapter_no = int(elm.get_attribute('innerHTML').split()[1].split('\t')[0])
        latest = data['names'][name]['latest']
        if chapter_no>latest:
            url = elm.get_attribute('href')
            driver.get(url)
            sleep(2)
            elems = driver.find_elements_by_css_selector("li.blocks-gallery-item")
            os.mkdir(os.path.join(os.getcwd(),str(chapter_no)))
            os.chdir(str(chapter_no))
            ct = 1
            for tag in elems:
                img_tag = tag.find_element_by_css_selector("figure>img")
                manga_url = img_tag.get_attribute("src")
                data = requests.get(manga_url)
                sleep(1)
                if data.status_code == 200:
                    with open(f"{ct}.jpg",'wb') as f:
                        f.write(data.content)
                ct+=1
except Exception as e:
    print(e)
    pass
driver.close()