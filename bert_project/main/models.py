from django.db import models

class ProductInfo(models.Model):
    title = models.CharField(max_length=50, unique=True)
    link = models.TextField()
    imageURL = models.TextField()
    price = models.IntegerField()
    maker = models.TextField()
    category1 = models.TextField()
    category2 = models.TextField()
    
