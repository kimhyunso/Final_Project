from django.urls import path
from . import views

app_name = 'main'




urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('detail/<str:keyword>/', views.detail, name='detail'),
    path('reviews/', views.reviews, name='reviews'),
    path('result/', views.result, name='result'),
]
