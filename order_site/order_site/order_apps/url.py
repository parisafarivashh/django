from django.urls import path, include
from .views import ProfileView, ProductViewSet, CategoryViewSet, MesonViewSet, SignUp, Login
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('category', CategoryViewSet)
router.register('meson', MesonViewSet)
router.register('signup', SignUp)


urlpatterns = [
    path('root/', include(router.urls)),
    path('', Login.as_view()),
    path('profile/', ProfileView.as_view())
]
