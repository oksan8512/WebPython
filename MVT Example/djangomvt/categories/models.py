# categories/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Слаг")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Зображення")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class CategoryImage(models.Model):
    """Зображення, які використовуються в описі категорій"""
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='description_images',
        verbose_name="Категорія"
    )
    image = models.ImageField(upload_to='category_descriptions/', verbose_name="Зображення")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Завантажено")
    original_filename = models.CharField(max_length=255, blank=True, verbose_name="Оригінальна назва")
    
    class Meta:
        verbose_name = "Зображення опису"
        verbose_name_plural = "Зображення описів"
        ordering = ['-uploaded_at']

    def __str__(self):
        if self.category:
            return f"Зображення для {self.category.name}"
        return f"Непривʼязане зображення #{self.id}"