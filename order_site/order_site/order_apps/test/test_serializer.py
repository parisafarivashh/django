from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from ..serializers import ProductSerializer, ProfileSerializer, MesonSerializer,\
    CategorySerializer, OrderSerializer, ItemOrderSerializer
from ..models import CustomUser, Product, Profile, Meson, Category, ItemOrder, Order
from ..views import ProfileView


class SerializerTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = CustomUser.objects.create_superuser(name='admin', email='admin@emial.com',
                                                         phone='09126939555', password='admin123')
        self.profile = Profile.objects.create(user=self.admin)
        self.meson = Meson.objects.create(name="asal", city="shiraz", address="shiraz street khayam ",
                                     email="asal@email.com")
        self.category = Category.objects.create(name='cloths')
        self.product = Product.objects.create(name="pants", size="L", color="Blue",
                                         number=58, price=300, meson=self.meson, categories=self.category)
        self.product_2 = Product.objects.create(name="hat", size="L", color="Blue",
                                           number=30, price=30, meson=self.meson, categories=self.category)
        self.order = Order.objects.create(user=self.admin, paid=False)
        self.item_order = ItemOrder.objects.create(product=self.product, order=self.order, count=2)

    def test_serializer_product(self):

        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/root/product/', follow=True)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_serializer_profile(self):
        self.client.force_authenticate(user=self.admin, token=self.admin.auth_token)
        response = self.client.get('/profile/')
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        self.assertTrue(response.data, serializer.data)

    def test_serializer_meson(self):
        meson = Meson.objects.all()
        serializer = MesonSerializer(meson, many=True)
        self.assertTrue(serializer.data[0]['name'], self.meson.name)

    def test_serializer_category(self):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        self.client.force_authenticate(user=self.admin, token=self.admin.auth_token)
        response = self.client.get('/root/category/')
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(serializer.data[0]['name'], self.category.name)

    def test_serializer_order(self):
        self.client.force_authenticate(user=self.admin, token=self.admin.auth_token)
        response = self.client.get('/root/order/basket/')
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        self.assertEqual(serializer.data, response.data)

    def test_serializer_itemorder(self):
        item_order = ItemOrder.objects.all()
        serializer = ItemOrderSerializer(item_order, many=True)
        # print(serializer.data[0]['product']['name'])
        self.assertEqual(serializer.data[0]['product']['name'], self.product.name)












