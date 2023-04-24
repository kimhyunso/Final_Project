import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def search(keyword):

    keys = []
    columns = ['title', 'link', 'image', 'price', 'maker', 'category1', 'category2']

    with open('API_KEY.txt', 'r') as key:
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

    url = f'https://openapi.naver.com/v1/search/shop?&query={keyword}'
    time.sleep(3.2)

    response = requests.get(url, headers=headers)
    # driver = webdriver.Chrome()
    line = response.json()

    for item in line['items']:
        item_list.append([item['title'], item['link'], item['image'], item['lprice'], item['maker'], item['category3'], item['category4']])


    return pd.DataFrame(item_list, columns=columns)

