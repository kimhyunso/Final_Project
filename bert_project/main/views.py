from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe
from django.utils import timezone
import pandas as pd
from .info import search, reviews
from .models import ProductInfo
import sqlite3


@require_safe
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


@require_http_methods(['POST'])
def info(request):
    keyword = request.POST['keyword']
    info_df = search(keyword)
    conn = sqlite3.connect('db.sqlite3')
    try:
        cursor = conn.cursor()
        sql = f"SELECT * FROM main_productinfo WHERE category1={keyword};"

        cursor.execute(sql)
        result = cursor.fetchall()

        if result != None:
            return redirect('main:detail', keyword)
        
        else:
            sql = "INSERT INTO main_productinfo(title, link, imageURL, price, maker, category1, category2) VALUES(?, ?, ?, ?, ?, ?, ?);"
            
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



