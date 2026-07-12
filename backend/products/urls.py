from django.urls import path, include
# products/urls.py
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrandViewSet, ProductCatalogViewSet, ProductViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category') # products/ olib tashlandi
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'catalog', ProductCatalogViewSet, basename='catalog')

urlpatterns = [
    path('', include(router.urls)),
]