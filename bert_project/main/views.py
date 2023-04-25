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

def info(request):
    info_df = search(request.POST['keyword'])
    conn = sqlite3.connect('db.sqlite3')
    info_df.to_sql('main_productinfo', conn, if_exists='replace',index =False)
    return redirect('main:detail')

