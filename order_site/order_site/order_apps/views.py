from django.db import transaction
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, Profile, CustomUser, Meson, Category, Order, ItemOrder
from .serializers import CustomUserSerializer, ProductSerializer,\
    ProfileSerializer, MesonSerializer, CategorySerializer, OrderSerializer, ItemOrderSerializer
from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import generics
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAdmin, IsOwn, ActionPermission
from rest_framework.permissions import IsAuthenticated, AllowAny


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
    permission_classes = (IsAdmin,)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwn)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Profile.objects.filter(user=user)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [ActionPermission,]
        return super().get_permissions()


class OrderViewList(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, IsOwn)
    serializer_class = OrderSerializer
    # queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user)
        return queryset

    @action(detail=True, url_path='paid', methods=['get'])
    def paid(self, request, *args, **kwargs):
        print(kwargs)
        order_id = kwargs['pk']
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()
            order = Order.objects.create(user=self.request.user)
            print(order)
            order.save()
            if len(Order.objects.filter(paid=False).filter(user=self.request.user))> 1:
                order.delete()

            return Response(status=status.HTTP_201_CREATED)


class ItemOrderViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):

    queryset = ItemOrder.objects.all()
    serializer_class = ItemOrderSerializer

    def perform_create(self, serializer):
        serializer.save(order=self.request.user.id_order)
