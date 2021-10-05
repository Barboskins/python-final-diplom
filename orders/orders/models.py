from django.db import models

"""Создаем модели и их дополнительные методы"""
class User(models.Model):
    __tablename__ = 'User'
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, null=False, unique=True)

class Shop(models.Model):
    __tablename__ = 'Shop'
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    url = models.URLField(null=False, unique=True)
    filename = models.CharField(max_length=200, null=False, unique=True)


class Category(models.Model):
    __tablename__ = 'Category'
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories')
    name = models.CharField(max_length=100)

class Product(models.Model):
    __tablename__ = 'Product'
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class ProductInfo(models.Model):
    __tablename__ = 'ProductInfo'
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    price_rrc = models.PositiveIntegerField()

class Parametr(models.Model):
    __tablename__='Parametr'
    name = models.CharField(max_length=200)

class ProductParametr(models.Model):
    __tablename__ = "ProductParametr"
    product_info = models.ForeignKey(ProductInfo, blank=True, on_delete=models.CASCADE)
    parametr = models.ForeignKey(Parametr, blank=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

class Order(models.Model):
    __tablename__ = "Order"
    user = models.ForeignKey(Parametr, blank=True, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    state = models.BooleanField()

class OrderItem(models.Model):
    __tablename__ = "OrderItem"
    order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Contact(models.Model):
    __tablename__ = "contact"
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    phone = models.CharField(max_length=20, verbose_name='Телефон')





