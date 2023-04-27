from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe
from django.utils import timezone
import pandas as pd
import numpy as np
from .info import search, comment_reviews, predict_sentiment
from .forms import ProductInfoForm, ProductSearchForm
from .models import ProductInfo
import sqlite3
from django.conf import settings
import re
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from django.core.files.storage import FileSystemStorage


@require_safe
def index(request):
    return render(request, 'main/index.html')


@require_safe
def detail(request, keyword):
    context = {
        'lists' : ProductInfo.objects.distinct().filter(category1=keyword),
    }
    return render(request, 'main/detail.html', context)



def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


@require_http_methods(['POST'])
def info(request):
    keyword = request.POST['keyword']
    info_df = search(keyword)
    conn = sqlite3.connect('db.sqlite3')
    try:
        cursor = conn.cursor()
        sql = "INSERT OR IGNORE INTO main_productinfo(title, link, imageURL, price, maker, category1, category2) VALUES(?, ?, ?, ?, ?, ?, ?);"
        
        rows = []
        for idx, row in info_df.iterrows():
            rows.append(row)


        cursor.executemany(sql, rows)
        conn.commit()
        conn.close()

    except:
        conn.rollback()
        return redirect('main:index')

    return redirect('main:detail', keyword)


@require_http_methods(['POST'])
def reviews(request):
    link = request.POST['link']

    reviews_df = comment_reviews(link)

    # 여기부터


    tokenizer = settings.TOKENIZER_KOBERT
    model = settings.MODEL_KOBERT

    result_bert = predict_sentiment(reviews_df['comments'][0], tokenizer, model)
    print(result_bert)
    
    # 긍정리뷰와 부정리뷰 분류할 빈 리스트
    good_reviews = []
    bad_reviews = []
    
    # 평균 리뷰 점수를 구하고, 긍정 부정 리뷰를 분류하는 코드
    score = 0
    sum = 0
    cnt = 0
    
    for review in reviews_df['comments']:
        
        if len(review) > 400:
            result_bert = predict_sentiment(review[-400:], tokenizer, model)
        else:
            result_bert = predict_sentiment(review, tokenizer, model)
        score = result_bert[0]
        sum += score
        cnt += 1
        
        if result_bert[1] == '긍정':
            good_reviews.append(review)
        else:
            bad_reviews.append(review)
    
    print('평균점수: ', round(sum / cnt, 2))
    
    good_token = tokenizer(good_reviews)
    bad_token = tokenizer(bad_reviews)
    
    font_path = r'C:/Windows/Fonts/malgun.ttf'
    
    tfidfv = TfidfVectorizer().fit_transform(good_token)
    wc = WordCloud(font_path=font_path, background_color='white', max_font_size=30, scale=7).generate_from_frequencies(tfidfv.vocabulary_)
    wc.to_image(os.getcwd()+'./media/good_reviews.png')
    
    # filename = "good_reviews.png"
    # wc_image = wc.to_image()
    # with fs.open(filename, 'wb') as f:
    #     wc_image.save(f, 'PNG')
    
    
    tfidfv = TfidfVectorizer().fit_transform(bad_token)
    wc = WordCloud(font_path=font_path, background_color='white', max_font_size=30, scale=7).generate_from_frequencies(tfidfv.vocabulary_)
    wc.to_image(os.getcwd()+'./media/bad_reviews.png')
    # filename = "bad_reviews.png"
    # wc_image = wc.to_image()
    # with fs.open(filename, 'wb') as f:
    #     wc_image.save(f, 'PNG')
        
    
    
    # context = {'target_sentence':reviews_df['comments'][0], 'result_bert':result_bert}
    
    # return render(request, 'main/index.html', context)



def tokenizer(sentence):
    okt = Okt()
    stopwords = ['하다', '힘그셨을텐데', '훌륭하다']
    sentence = re.sub("[^\s0-9a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]", "", str(sentence))
    raw_pos_tagged = okt.pos(sentence, stem=True) # POS Tagging with stemming

    sentence_tokenized = []
    for token, pos in raw_pos_tagged:
        if (len(token) != 1) & (pos in ["Noun", "Verb", "Adverb", "Adjective"]) & (token not in stopwords):
            sentence_tokenized.append(token)
            
    return sentence_tokenized
