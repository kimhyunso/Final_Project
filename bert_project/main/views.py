from django.shortcuts import render
from django.utils import timezone
from .models import POST
import pandas as pd

def index(request):
    posts = POST.objects.all().order_by('-pk')
    current_time = timezone.now()
    
    context = {'posts':posts}
    return render(request, 'main/index.html', context)

def detail(request):
    context={}
    return render(request, 'main/detail.html', context)
