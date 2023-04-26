from django import forms
from .models import ProductInfo

class ProductSearchForm(forms.Form):
    search = forms.CharField(
        error_messages={
            'required' : '제품을 입력해 주세요.'
        },
        max_length=50,
        required=True,
        widget={


        },
    )

class ProductInfoForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        exclude = ('link', )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }