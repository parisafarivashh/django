from django.shortcuts import render
from rest_framework.response import Response

from .models import Product, Profile, CustomUser, Meson, Category
from .serializers import CustomUserSerializer, ProductSerializer, ProfileSerializer, MesonSerializer, CategorySerializer
from rest_framework import viewsets
from rest_framework.viewsets import generics
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAdmin, IsOwn
from rest_framework.permissions import IsAuthenticated


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({
            'user': user.pk,
            'email_user': user.email,
            'phone_user': user.phone
        })


class SignUp(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class MesonViewSet(viewsets.ModelViewSet):
    queryset = Meson.objects.all()
    serializer_class = MesonSerializer
    permission_classes = [IsAdmin,]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin,]


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwn,]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

