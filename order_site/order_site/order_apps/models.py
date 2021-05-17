from django.db import models
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