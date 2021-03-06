from datetime import datetime

from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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

    @property
    def id_order(self):
        id_order = self.orders.last()
        return id_order


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    code_postie = models.CharField(max_length=8)


class Meson(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    email = models.EmailField(unique=True, max_length=50)
    event_start = models.DateTimeField(blank=True, null=True)
    event_end = models.DateTimeField(blank=True, null=True)


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
    photo = models.ImageField(upload_to='products')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)


    @property
    def cost(self):
        cost = 0
        for item in self.items.all():
            cost += item.cost
        return cost


class ItemOrderManager(models.Manager):
    def create(self, **kwargs):
        # print("kwargs", kwargs)
        product = kwargs.get('product', None)
        order = kwargs.get('order', None)
        count = kwargs.get('count', None)

        price = product.price
        with transaction.atomic():
            instance = super().create(price=price, product=product, order=order, count=count)
            if product:
                # print(product.number)
                product.number = product.number - count
                if product.number < 0:
                    raise ValueError('order number not available')
                product.save()
                # print(product.number)
                return instance


class ItemOrder(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('order', on_delete=models.CASCADE, related_name='items')
    price = models.FloatField()
    count = models.IntegerField()

    objects = ItemOrderManager()

    @property
    def cost(self):
        return self.count * self.price

    def __str__(self):
        return self.product

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        super(ItemOrder, self).delete(*args, **kwargs)
        self.product.number += self.count
        self.product.save()
