# products/admin.py

from django.contrib import admin
from .models import Category, Product
from .models import CategoryBanner

admin.site.register(CategoryBanner)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock', 'category')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'brand')
    prepopulated_fields = {'slug': ('name',)}
