from django.db import models

"""Создаем модели и их дополнительные методы"""
class User(models.Model):
    name = models.CharField()
    lastname = models.CharField()
    username = models.CharField()
    email = models.EmailField()

class Shop(models.Model):
    name = models.CharField()
    url = models.URLField()
    filename = models.FilePathField()

class Category(models.Model):
    shops = models.ManyToManyField(Shop)
    name = models.CharField()

class Product(models.Model):
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    name = models.CharField()

class ProductInfo(models.Model):
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, blank=True, on_delete=models.CASCADE)
    name = models.CharField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    price_rrc = models.IntegerField()

class Parametr(models.Model):
    name = models.CharField()

class ProductParametr(models.Model):
    product_info = models.ForeignKey(ProductInfo, blank=True, on_delete=models.CASCADE)
    parametr = models.ForeignKey(Parametr, blank=True, on_delete=models.CASCADE)
    value = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(Parametr, blank=True, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    status = models.CharField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Contact(models.Model):
    type = models.CharField()
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    value = models.IntegerField()





