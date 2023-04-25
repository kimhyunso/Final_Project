from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe
from django.utils import timezone
import pandas as pd
from .info import search
from .models import ProductInfo

import sqlite3


def index(request):
    return render(request, 'main/index.html')

def detail(request):
    context={}
    return render(request, 'main/detail.html', context)

def info(request):
    info_df = search(request.POST['keyword'])
    conn = sqlite3.connect('db.sqlite3')
    info_df.to_sql('main_productinfo', conn, if_exists='replace',index =False)

    

    return redirect('main:detail')

