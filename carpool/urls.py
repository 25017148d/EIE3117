from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, MeAPIView, RouteViewSet, HealthAPIView


router = DefaultRouter()
router.register('routes', RouteViewSet, basename='routes')


urlpatterns = [
    path('health/', HealthAPIView.as_view()),
    path('auth/register/', RegisterAPIView.as_view()),
    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/me/', MeAPIView.as_view()),
    path('', include(router.urls)),
]
