from django.contrib import admin
from .models import Category, Brand, Product, BundleItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Agar modelda 'slug' bo'lsa qoldiring, bo'lmasa olib tashlang
    prepopulated_fields = {'slug': ('name',)} 
    list_display = ['name'] # 'parent' maydoni modelda bo'lsa qoldiring

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 'ProductImageInline' ni o'chirib tashladik
    list_display = ['name', 'sku', 'price', 'stock', 'category', 'is_active', 'is_bundle']
    list_filter = ['category', 'brand', 'is_active', 'is_bundle']
    search_fields = ['name', 'sku']

@admin.register(BundleItem)
class BundleItemAdmin(admin.ModelAdmin):
    list_display = ['bundle', 'component', 'quantity']
    search_fields = ['bundle__name', 'component__name']