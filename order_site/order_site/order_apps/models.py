from datetime import datetime

from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, phone, password):
        if not phone:
            raise ValueError('the user must have a phone number')

        email = self.normalize_email(email)
        user = self.model(name=name, email=email, phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, phone, password):
        user = self.create_user(name, email, phone, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, blank=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    code_postie = models.CharField(max_length=8)


class Meson(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    email = models.EmailField(unique=True, max_length=50)
    event_start = models.DateTimeField(default=datetime.now)
    event_end = models.DateTimeField()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10, choices=[('L', 'L'), ('M', 'M'), ('X', 'X'), ('XL', 'XL'), ('XXL', 'XXL'), ('NO SIZE', 'NO SIZE')])
    color = models.CharField(max_length=10, choices=[('Red', 'Red'), ('Blue', 'Blue'), ('White', 'White'), ('Black', 'Black'), ('Brown', 'Brown'), ('colorful', 'colorful')])
    number = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    meson = models.ForeignKey('Meson', on_delete=models.CASCADE, related_name='products')
    categories = models.ForeignKey('Category', on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)


class ItemOrderManager(models.Manager):
    def create(self, **kwargs):
        print("kwargs", kwargs)
        product = kwargs.get('product', None)
        order = kwargs.get('order', None)
        count = kwargs.get('count', None)

        price = product.price
        with transaction.atomic():
            instance = super().create(price=price, product=product, order=order, count=count)
            if product:
                print(product.number)
                product.number = product.number - count
                if product.number < 0:
                    raise ValueError('order number not available')
                product.save()
                print(product.number)
                return instance


class ItemOrder(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('order', on_delete=models.CASCADE)
    price = models.FloatField()
    count = models.IntegerField()

    objects = ItemOrderManager()

    @property
    def cost(self):
        return self.count * self.price

    def __str__(self):
        return self.product

