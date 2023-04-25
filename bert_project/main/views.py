from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .info import search
from .models import ProductInfo
# from .forms import ProductInfoForm
import sqlite3


def index(request):
    return render(request, 'main/index.html')

def detail(request):
    # product_info = ProductInfoForm()
    # print(product_info)
    context={}
    return render(request, 'main/detail.html', context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def info(request):
    keyword = request.POST['keyword']
    info_df = search(keyword)
    conn = sqlite3.connect('db.sqlite3')
    info_df.to_sql('main_productinfo', conn, if_exists='replace',index =False)
    return redirect('main:detail')

