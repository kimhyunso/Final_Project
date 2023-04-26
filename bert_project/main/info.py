import os
import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
from selenium.webdriver.common.by import By


def search(keyword):

    keys = []
    columns = ['title', 'link', 'image', 'price', 'maker', 'category1', 'category2']

    scriptpath = os.path.dirname(__file__)
    filename = os.path.join(scriptpath, 'API_KEY.txt')
    
    with open(filename, 'r', encoding='utf-8') as key:
        for line in key.readlines():
            text = line.strip()
            if text != '':
                keys.append(text.split(':')[1])

    headers = {
        'X-Naver-Client-Id' : keys[0],
        'X-Naver-Client-Secret' : keys[1],
    }

    item_list = []
    columns = ['title', 'link', 'image', 'price', 'maker', 'category1', 'category2']

    url = f'https://openapi.naver.com/v1/search/shop?&query={keyword}&display=8'

    response = requests.get(url, headers=headers)
    time.sleep(2.8)
    
    line = response.json()
    for item in line['items']:
        item_list.append([item['title'], item['link'], item['image'], item['lprice'], item['maker'], item['category3'], item['category4']])


    return pd.DataFrame(item_list, columns=columns)

def comment_reviews(link):
    reviews = []

    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(2.3)

    driver.find_element(By.CSS_SELECTOR, '#wrap > div.product_bridge_product__n_89z > a:nth-child(5)').click()
    time.sleep(3.2)

    page_no = 1
    for _ in range(5):
        if page_no == 11:
            driver.find_element(By.CSS_SELECTOR, '#section_review > div.pagination_pagination__JW7zT > a.pagination_next__3_3ip').click()
            page_no = 2
            
        time.sleep(3.8)
        driver.find_element('xpath', f'//*[@id="section_review"]/div[3]/a[{page_no}]').click()
        
        time.sleep(2.8)
        response = driver.find_elements('xpath', '//*[@id="section_review"]/ul/li/div[2]/div[1]/p')
        
        for review in response:
            reviews.append(review.text)
        
        page_no += 1
    
    return pd.DataFrame(reviews, columns=['comments'])


