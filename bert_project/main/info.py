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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--headless')

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

    driver = webdriver.Chrome(chrome_options=chrome_options)  # chrome_options jys 추가해봄
    driver.get(link)
    # time.sleep(2.3)
    
    # jys 대기 추가#####
    print(link)
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '#wrap > div.product_bridge_product__n_89z > a:nth-child(5)')))
    element.click()
    ###################

    # driver.find_element(By.CSS_SELECTOR, '#wrap > div.product_bridge_product__n_89z > a:nth-child(5)').click()
    # time.sleep(3.2)

    page_no = 1
    for _ in range(5):
        if page_no == 11:
            driver.find_element(By.CSS_SELECTOR, '#section_review > div.pagination_pagination__JW7zT > a.pagination_next__3_3ip').click()
            page_no = 2
            
        # time.sleep(3.8)
        # driver.find_element('xpath', f'//*[@id="section_review"]/div[3]/a[{page_no}]').click()
        
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="section_review"]/div[3]/a[{page_no}]')))
        element.click()
        
        # time.sleep(2.8)
        # response = driver.find_elements('xpath', '//*[@id="section_review"]/ul/li/div[2]/div[1]/p')
        
        elements = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="section_review"]/ul/li/div[2]/div[1]/p')))
        response = [element.text for element in elements]
        
        
        for review in response:
            reviews.append(review)
        
        page_no += 1
    
    driver.quit()  # jys 추가
    return pd.DataFrame(reviews, columns=['comments'])



def predict_sentiment(sentence, tokenizer, model):

    SEQ_LEN = 256

    # Tokenizing / Tokens to sequence numbers / Padding
    encoded_dict = tokenizer.encode_plus(text=re.sub("[^\s0-9a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]", "", sentence),
                                         padding='max_length',
                                         truncation = True,
                                         max_length=SEQ_LEN) # SEQ_LEN == 256

    token_ids = np.array(encoded_dict['input_ids']).reshape(1, -1) # shape == (1, 256) : like appending to a list
    token_masks = np.array(encoded_dict['attention_mask']).reshape(1, -1)
    token_segments = np.array(encoded_dict['token_type_ids']).reshape(1, -1)

    new_inputs = (token_ids, token_masks, token_segments)

    # Prediction
    prediction = model.predict(new_inputs)
    predicted_probability = np.round(np.max(prediction) * 2.5, 2)
    predicted_class = ['부정', '긍정'][np.argmax(prediction, axis=1)[0]]
    
    if predicted_class == '긍정':
        score = 2.5 + predicted_probability
    else:
        score = 2.5 - predicted_probability
    
    result = [score, predicted_class]

    return result