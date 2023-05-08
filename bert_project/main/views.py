from django.http import Http404, JsonResponse
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
import json
from PIL import Image
from django.db.models import Q





@require_safe
def index(request):
    return render(request, 'main/index.html')


@require_safe
def detail(request, keyword):
    context = {
        'lists' : ProductInfo.objects.distinct().filter(Q(title__icontains=keyword) | Q(category1=keyword)),
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
    jsonObject = json.loads(request.body)
    link = jsonObject.get('link')
    reviews_df = comment_reviews(link)

    tokenizer = settings.TOKENIZER_KOBERT
    model = settings.MODEL_KOBERT

    result_bert = predict_sentiment(reviews_df['comments'][0], tokenizer, model)
    
    # 긍정리뷰와 부정리뷰 분류할 빈 리스트
    good_comment = ''
    bad_comment = ''
    
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
            good_comment += review
        else:
            bad_comment += review

    
    

    good_token = sentence_tokenizer(good_comment)
    bad_token = sentence_tokenizer(bad_comment)

    n = 5

    counter = Counter(good_token)
    good_frequency = counter.most_common(n)

    counter = Counter(bad_token)
    bad_frequency = counter.most_common(n)

    font_path = r'C:/Windows/Fonts/malgunbd.ttf'

    icon = Image.open('./media/thumb_up.png')
    mask = Image.new("RGB", icon.size, (255,255,255))
    mask.paste(icon,icon)
    mask = np.array(mask)

    wc = WordCloud(font_path=font_path, background_color='white', colormap='ocean', mask=mask).generate_from_frequencies(count_vectorization(good_token))
    wc.to_file('./media/good_reviews.png')


    icon = Image.open('./media/thumb_down.png')
    mask = Image.new("RGB", icon.size, (255,255,255))
    mask.paste(icon,icon)
    mask = np.array(mask)

    wc = WordCloud(font_path=font_path, background_color='white', colormap='ocean', mask=mask).generate_from_frequencies(count_vectorization(bad_token))
    wc.to_file('./media/bad_reviews.png')


    score = '%.2f' % (sum / cnt)

    context = {
        'score' : score,
        'eval' : result_bert[1],
        'good_frequency' : good_frequency,
        'bad_frequency' : bad_frequency,
    }

    return JsonResponse(context)


def count_vectorization(token):
    vector = TfidfVectorizer()
    bow_vect = vector.fit_transform(token)
    word_list = vector.get_feature_names()
    count_list = bow_vect.toarray().sum(axis=0)
    word_count_dict = dict(zip(word_list, count_list))
    return word_count_dict


def sentence_tokenizer(sentence):
    okt = Okt()
    stopwords = ['하다', '힘그셨을텐데', '세탁기', '제품', '있다', '자다', '배송', '기사', '없다', '같다', '가구', '해주다', '되다', '너무', '작다', '설치', '않다', '되다', '되어다']
    sentence = re.sub("[^\s0-9a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]", "", sentence)
    raw_pos_tagged = okt.pos(sentence, stem=True)

    sentence_tokenized = []

    for token, pos in raw_pos_tagged:
        if (len(token) != 1) & (pos in ["Noun", "VerbPrefix", "Adverb", "Adjective"]) & (token not in stopwords):
            sentence_tokenized.append(token)
            
    return sentence_tokenized

@require_http_methods(['GET', 'POST'])
def result(request):



    good_comments = request.GET['good_comment'].split(',')
    bad_comments = request.GET['bad_comment'].split(',')

    context = {
        'score' : request.GET['score'],
        'eval' : request.GET['eval'],
        'good_comments' : good_comments,
        'bad_comments' : bad_comments,
    }
    return render(request, 'main/result.html', context)