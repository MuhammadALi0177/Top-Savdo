from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet # ProductViewSet ni bu yerdan o'chiring!

router = DefaultRouter()
# router.register(r'products', ProductViewSet, basename='product') # 🔴 BUNI O'CHIRING
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]