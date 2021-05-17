from django.shortcuts import render
from .models import Product, Profile, CustomUser, Meson, Category
from .serializers import CustomUserSerializer, ProductSerializer, ProfileSerializer, MesonSerializer, CategorySerializer
from rest_framework import viewsets
from rest_framework.viewsets import generics


class SignUp(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class MesonViewSet(viewsets.ModelViewSet):
    queryset = Meson.objects.all()
    serializer_class = MesonSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

