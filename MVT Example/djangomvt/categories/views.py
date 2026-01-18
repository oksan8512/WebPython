from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os

from .models import Category, CategoryImage

def show_categories(request):
    categories = Category.objects.all()
    return render(request, "categories.html", {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        # Перевірка, чи slug унікальний
        if Category.objects.filter(slug=slug).exists():
            messages.error(request, 'Категорія з таким slug вже існує')
            return render(request, 'add_category.html')
        
        # Створення категорії
        category = Category.objects.create(
            name=name,
            slug=slug,
            description=description,
            is_active=is_active,
            image=image
        )
        
        messages.success(request, f'Категорія "{name}" успішно додана!')
        return redirect('categories:show_categories')
    
    return render(request, 'add_category.html')

@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    """Завантаження зображення з TinyMCE"""
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'Файл не знайдено'}, status=400)
    
    file = request.FILES['file']
    
    # Перевірка типу файлу
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        return JsonResponse({'error': 'Недозволений тип файлу'}, status=400)
    
    # Створення запису в базі
    category_image = CategoryImage.objects.create(
        image=file,
        original_filename=file.name
    )
    
    return JsonResponse({
        'location': category_image.image.url,
        'image_id': category_image.id
    })