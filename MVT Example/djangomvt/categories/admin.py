from django.contrib import admin
from .models import Category, CategoryImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'original_filename', 'uploaded_at']
    list_filter = ['category', 'uploaded_at']
    search_fields = ['original_filename']