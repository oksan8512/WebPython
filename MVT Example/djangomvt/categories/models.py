from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    slug = models.SlugField(max_length=120, verbose_name="Слаг")  # Прибрали unique=True
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Зображення")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)