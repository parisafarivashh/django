from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import ProfileView, ProductViewSet, CategoryViewSet\
    , MesonViewSet, SignUp, Login, OrderViewList, ItemOrderViewSet, ChangePasswordView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('category', CategoryViewSet)
router.register('meson', MesonViewSet)
# router.register('signup', SignUp, basename='signup')
router.register('item_order', ItemOrderViewSet)
router.register('order', OrderViewList, basename='order')


urlpatterns = [
    path('root/', include(router.urls)),
    path('', SignUp.as_view()),
    path('login', Login.as_view()),
    path('profile/', ProfileView.as_view()),
    path('change_password/', ChangePasswordView.as_view())

]
urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)