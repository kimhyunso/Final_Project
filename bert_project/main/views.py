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
from . import inference_bert

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

    # target_sentence = request.POST['target_sentence']

    tokenizer = settings.TOKENIZER_KOBERT
    model = settings.MODEL_KOBERT

    result_bert = predict_sentiment(reviews_df['comments'][0], tokenizer, model)
    print(result_bert)
    # context = {'target_sentence':reviews_df['comments'][0], 'result_bert':result_bert}
    
    # return render(request, 'main/index.html', context)

