from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, RegistrationViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', RegistrationViewSet, basename='register')

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('', include(router.urls))
]