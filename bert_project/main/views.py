from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe
from django.utils import timezone
from .models import POST
import pandas as pd
from .info import search



def index(request):
    posts = POST.objects.all().order_by('-pk')
    current_time = timezone.now()
    
    context = {'posts':posts}
    return render(request, 'main/index.html', context)

def detail(request):
    context={}
    return render(request, 'main/detail.html', context)


def info(request):
    # search()

    return redirect('main:detail')

