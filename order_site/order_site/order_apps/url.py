from django.urls import path, include
from .views import ProfileView, ProductViewSet, CategoryViewSet, MesonViewSet, SignUp
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('category', CategoryViewSet)
router.register('meson', MesonViewSet)
router.register('signup', SignUp)


urlpatterns = [
    path('', include(router.urls)),
    path('profile/<int:pk>', ProfileView.as_view())
]
