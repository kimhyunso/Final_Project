from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe
from django.utils import timezone
import pandas as pd
from .info import search
from .forms import ProductInfoForm, ProductSearchForm
from .models import ProductInfo
import sqlite3


def index(request):
    return render(request, 'main/index.html')

@require_safe
def detail(request, keyword):
    context = {
        'lists' : ProductInfo.objects.filter(category1=keyword),
    }
    return render(request, 'main/detail.html', context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def info(request):
    keyword = request.POST['keyword']
    info_df = search(keyword)
    conn = sqlite3.connect('db.sqlite3')
    try:
        cursor = conn.cursor()
        sql = 'INSERT INTO main_productinfo(title, link, imageURL, price, maker, category1, category2) VALUES(?, ?, ?, ?, ?, ?, ?);'
        
        rows = []
        for idx, row in info_df.iterrows():
            rows.append(row)

        cursor.executemany(sql, rows)
        conn.commit()
        conn.close()

    except:
        conn.rollback()
        return Http404('Not Found Page!')

    return redirect('main:detail', keyword)
