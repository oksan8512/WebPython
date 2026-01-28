from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category
from django.utils.text import slugify
import requests
from django.core.files.base import ContentFile
import uuid

def show_categories(request):
    categories = Category.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'categories.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image_url = request.POST.get('image_url')
        image_file = request.FILES.get('image_file')
        
        if not name:
            messages.error(request, 'Назва категорії обов\'язкова!')
            return render(request, 'add_category.html')
        
        try:
            slug = slugify(name)
            
            category = Category(
                name=name,
                slug=slug,
                description=description
            )
            
            # Спосіб 1: Завантаження файлу
            if image_file:
                category.image = image_file
            
            # Спосіб 2: URL зображення
            elif image_url:
                try:
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    
                    file_name = image_url.split('/')[-1].split('?')[0]
                    if '.' not in file_name:
                        file_name = f'{uuid.uuid4()}.jpg'
                    
                    category.image.save(
                        file_name,
                        ContentFile(response.content),
                        save=False
                    )
                except requests.exceptions.RequestException as e:
                    messages.warning(request, f'Не вдалося завантажити зображення з URL: {str(e)}')
            
            category.save()
            messages.success(request, 'Категорію успішно додано!')
            return redirect('categories:show_categories')
            
        except Exception as e:
            messages.error(request, f'Помилка при створенні категорії: {str(e)}')
    
    return render(request, 'add_category.html')


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image_url = request.POST.get('image_url')
        image_file = request.FILES.get('image_file')
        remove_image = request.POST.get('remove_image')
        
        if not name:
            messages.error(request, 'Назва категорії обов\'язкова!')
            return render(request, 'edit_category.html', {'category': category})
        
        try:
            category.name = name
            category.slug = slugify(name)
            category.description = description
            
            # Видалення зображення
            if remove_image:
                if category.image:
                    category.image.delete()
                    category.image = None
            
            # Завантаження нового файлу
            if image_file:
                if category.image:
                    category.image.delete()
                category.image = image_file
            
            # URL зображення
            elif image_url and not remove_image:
                try:
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    
                    if category.image:
                        category.image.delete()
                    
                    file_name = image_url.split('/')[-1].split('?')[0]
                    if '.' not in file_name:
                        file_name = f'{uuid.uuid4()}.jpg'
                    
                    category.image.save(
                        file_name,
                        ContentFile(response.content),
                        save=False
                    )
                except requests.exceptions.RequestException as e:
                    messages.warning(request, f'Не вдалося завантажити зображення з URL: {str(e)}')
            
            category.save()
            messages.success(request, 'Категорію успішно оновлено!')
            return redirect('categories:show_categories')
            
        except Exception as e:
            messages.error(request, f'Помилка при оновленні категорії: {str(e)}')
    
    return render(request, 'edit_category.html', {'category': category})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        
        # Видаляємо зображення якщо є
        if category.image:
            category.image.delete()
        
        category.delete()
        messages.success(request, f'Категорію "{category_name}" успішно видалено!')
        return redirect('categories:show_categories')
    
    return render(request, 'delete_category.html', {'category': category})