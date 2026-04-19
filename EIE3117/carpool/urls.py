from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterAPIView,
    MeAPIView,
    RouteViewSet,
    HealthAPIView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
)


router = DefaultRouter()
router.register('routes', RouteViewSet, basename='routes')


urlpatterns = [
    path('health/', HealthAPIView.as_view()),
    path('auth/register/', RegisterAPIView.as_view()),
    # Use cookie-backed endpoints: refresh token is stored in an HttpOnly cookie.
    path('auth/token/', CookieTokenObtainPairView.as_view()),
    path('auth/token/refresh/', CookieTokenRefreshView.as_view()),
    path('auth/me/', MeAPIView.as_view()),
    path('', include(router.urls)),
]
