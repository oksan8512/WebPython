from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify
import os

from .models import Category, CategoryImage


def show_categories(request):
    categories = Category.objects.all()
    return render(request, "categories.html", {'categories': categories})


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')
        
        # Автоматична генерація slug
        base_slug = slugify(name, allow_unicode=False)
        slug = base_slug
        
        # Перевірка унікальності slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        try:
            # Створення категорії (is_active=True за замовчуванням)
            category = Category.objects.create(
                name=name,
                slug=slug,
                description=description,
                image=image
            )
            
            messages.success(request, f'Категорія "{name}" успішно додана!')
            return redirect('categories:show_categories')
        except Exception as e:
            messages.error(request, f'Помилка при створенні категорії: {str(e)}')
            return render(request, 'add_category.html')
    
    return render(request, 'add_category.html')


@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    """Завантаження зображення з TinyMCE"""
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'Файл не знайдено'}, status=400)
    
    file = request.FILES['file']
    
    # Перевірка типу файлу
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        return JsonResponse({'error': 'Недозволений тип файлу'}, status=400)
    
    try:
        # Створення запису в базі
        category_image = CategoryImage.objects.create(
            image=file,
            original_filename=file.name
        )
        
        return JsonResponse({
            'location': category_image.image.url,
            'image_id': category_image.id
        })
    except Exception as e:
        return JsonResponse({'error': f'Помилка завантаження: {str(e)}'}, status=500)