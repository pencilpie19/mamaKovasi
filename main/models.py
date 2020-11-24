from django.utils.timezone import now
from itertools import chain
from ckeditor.fields import RichTextField

from django.db import models

# Create your models here.
class Pet(models.Model):
    name=models.CharField(max_length=10,verbose_name="Evcil Hayvan İsmi")
    file = models.FileField(upload_to="pet",blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length=15,verbose_name="Kategori İsmi")
    pet=models.ForeignKey(Pet,related_name="categories",on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} | {} ".format(self.pet, self.name)

class Product(models.Model):
    name=models.CharField(max_length=80,verbose_name="Ürün İsmi")
    file = models.FileField(upload_to="product",blank=True,null=True)
    category=models.ForeignKey(Category,related_name="products",on_delete=models.CASCADE,null=True,blank=True)
    detail=RichTextField()
    price=models.FloatField(verbose_name="Ürün Fiyatı")
    brand=models.CharField(max_length=80,verbose_name="Ürün Markası",blank=True,null=True)
    weight=models.FloatField(verbose_name="Ürün Ağırlığı (Kg Cinsinden)",blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    def get_related_products(self):
        listOne=Product.objects.filter(category__pet=self.category.pet).exclude(id=self.id).order_by("-created_date")[:4]

        return listOne

    def __str__(self):
        return self.name

class Help(models.Model):
    name=models.CharField(max_length=80,verbose_name="Ad Soyad")
    email=models.EmailField(verbose_name="E-Posta Adresi")
    message=models.TextField(verbose_name="Mesajınız")
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " kişisinin mesajı..."

