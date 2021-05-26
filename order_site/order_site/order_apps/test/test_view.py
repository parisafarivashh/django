from django.test import Client, TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from ..models import CustomUser, Product, Profile, Order, ItemOrder,Meson , Category
from rest_framework.test import APIRequestFactory, force_authenticate
from ..views import ProductViewSet, CategoryViewSet, ProfileView, OrderViewList, MesonViewSet, Login


class ViewTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_superuser(name="user", email="user@email.com",
                                                        phone="09126939588", password="user123")
        profile = Profile.objects.create(user=self.user)
        order = Order.objects.create(user=self.user, paid=False)
        # print(Order.objects.get(user=self.user))
        self.meson = Meson.objects.create(name="asal", city="shiraz", address="shiraz street khayam ", email="asal@email.com")
        self.category = Category.objects.create(name='cloths')
        self.product = Product.objects.create(name="pants", size="L", color="Blue",
                                         number=58, price=300, meson=self.meson, categories=self.category)
        item_order = ItemOrder.objects.create(product=self.product, order=order, count=2)

    def test_view_login(self):
        request = self.factory.post('login/', {"username": "09126939588", "password": "user123"})
        response = Login.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['email_user'] , self.user.email)

    def test_signup(self):
        c = Client()
        response = c.post('',
                          {"name": "user_2", "email": "user@email.com", "phone": "09012345678", "password": "user2123"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_product(self):
        view = ProductViewSet.as_view({'get': 'list'})
        request = self.factory.get('/root/product/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]['name'], self.product.name)

    # def test_create_product(self):
    #     request = self.factory.post('/root/product/', {"name": "pants", "size": "L", "color": "Blue", "number": 58, "price": 300, "meson": self.meson, "categories": self.category})
    #     force_authenticate(request, user=self.user)
    #     response = ProductViewSet.as_view({'post': 'create'})(request)
    #     self.assertEqual(response.status_code, 201)

    def test_create_category(self):
        request = self.factory.post('/root/category/', {"name": "cloths"})
        force_authenticate(request, user=self.user)
        response = CategoryViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"name": "cloths"})

    def test_profile(self):
        request = self.factory.get('profile/')
        force_authenticate(request, user=self.user)
        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data, "{'user': OrderedDict([('name', 'user'), ('email', 'user@email.com'), ('phone', '09126939588')]), 'code_postie': '', 'address': ''}")

    def test_list_order(self):
        request = self.factory.get('/root/order/basket/')
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = OrderViewList.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    # def test_create_meson(self):
    #     form_data ={'name': 'barana', 'city': 'qom', 'address': 'qom street kamyab',
    #                 'email': 'barana@email.com', 'event_start': '2021-02-01 00000:00',
    #                 'event_end': '2021-04-03 00:00:00'}
    #
    #     request = self.factory.post('/root/meson/', data=form_data)
    #
    #     force_authenticate(request, user=self.user, token=self.user.auth_token)
    #     response = MesonViewSet.as_view({'post': 'create'})(request)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     print(response.data)