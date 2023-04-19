from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # 127.0.0.1:8000/predict_sentiment/bert_input/
    path('bert_input/', views.bert_input, name='bert_input'),
    # 127.0.0.1:8000/predict_sentiment/bert_predict/
    path('bert_predict/', views.bert_predict, name='bert_predict'),
]