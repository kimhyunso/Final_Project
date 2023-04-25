# from django.forms import ModelForm, TextInput, CharField, IntegerField
# from .models import models


# class ProductInfoForm(ModelForm):
#     class Meta:
#         model = models
#         fields = ['title', 'link', 'imageURL', 'price', 'maker', 'category1', 'category2']
#         widgets = {
#             'title': CharField(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 300px;',
#                 'placeholder': 'title'
#                 }),
#             'link': TextInput(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 300px;',
#                 'placeholder': 'link'
#                 }),
#             'imageURL': TextInput(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 100px;',
#                 'placeholder': 'imageURL'
#             }),
#             'price': IntegerField(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 100px;',
#                 'placeholder': 'price'
#             }),
#             'maker': TextInput(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 100px;',
#                 'placeholder': 'maker'
#             }),
#             'category1': TextInput(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 100px;',
#                 'placeholder': 'category1'
#             }),
#             'category2': TextInput(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 100px;',
#                 'placeholder': 'category2'
#             }),
#         }