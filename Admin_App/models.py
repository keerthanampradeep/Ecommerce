from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=10)
    image=models.ImageField(upload_to="category",default="sample.jpg")


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_picture = models.ImageField(upload_to="picture")
    item_price = models.CharField(max_length=100)
    product_description= models.CharField(max_length=6)


   