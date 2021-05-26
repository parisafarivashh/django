from rest_framework.test import APIRequestFactory, force_authenticate
from django.test import TestCase
from ..models import CustomUser, Order, Profile, Product
from ..permissions import IsAdmin, IsOwn, ActionPermission
from rest_framework.permissions import AllowAny
from ..views import ProductViewSet


class PermissionTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = CustomUser.objects.create_superuser(name="admin", email="admin@email.com",
                                                         password="admin123", phone="09126939581")
        self.admin.is_staff = True
        self.user = CustomUser.objects.create_user(name="user", email="user@email.com",
                                                  password="user123", phone="09386917516")

    def test_permission_own(self):
        request = self.factory.get('profile/')
        force_authenticate(request, user=self.user)
        permission = IsOwn()
        has_permisiion = permission.has_permission(request, None)
        self.assertTrue(has_permisiion)

    def test_permission_admin(self):
        request = self.factory.get('/root/category/')
        request.user = self.admin
        permission = IsAdmin()
        has_permission = permission.has_permission(request, None)
        self.assertTrue(has_permission)

    def test_permission_action_list(self):
        request = self.factory.get('/root/product/')
        force_authenticate(request, user=self.user)
        view = ProductViewSet.as_view({'get': 'list'})
        if view.actions =='list':
            permission = AllowAny()
            has_permission = permission.has_permission(request, view=view.actions)
            self.assertTrue(has_permission)

    def test_permission_action_create(self):
        request = self.factory.post('/root/product/')
        force_authenticate(request, user=self.admin)
        view = ProductViewSet.as_view({'post': 'create'})
        if view.actions == 'create':
            permission = ActionPermission()
            has_permission = permission.has_permission(request, view=view.actions)
            self.assertEqual(has_permission, True)










