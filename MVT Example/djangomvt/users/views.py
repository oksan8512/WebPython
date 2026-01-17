from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .utils import compress_image
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model

# Отримуємо кастомну модель користувача
User = get_user_model()

# Create your views here.
def register(request):
    """
    View для реєстрації нового користувача
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Створюємо користувача але не зберігаємо в БД
                user = form.save(commit=False)
                
                # Додаємо дані з форми
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                
                # Обробка зображення
                if 'image' in request.FILES:
                    # Створюємо 3 версії зображення (маленьке, середнє, велике)
                    optimized_image_small, image_name_small = compress_image(
                        request.FILES['image'], 
                        size=(300, 300)
                    )
                    user.image_small.save(image_name_small, optimized_image_small, save=False)
                    
                    optimized_image_medium, image_name_medium = compress_image(
                        request.FILES['image'], 
                        size=(800, 800)
                    )
                    user.image_medium.save(image_name_medium, optimized_image_medium, save=False)
                    
                    optimized_image_large, image_name_large = compress_image(
                        request.FILES['image'], 
                        size=(1200, 1200)
                    )
                    user.image_large.save(image_name_large, optimized_image_large, save=False)
                
                # Зберігаємо користувача в БД
                user.save()
                
                # Автоматично входимо після реєстрації
                login(request, user)
                
                # Показуємо повідомлення про успіх
                messages.success(
                    request, 
                    f'Вітаємо, {user.first_name}! Ви успішно зареєструвалися!'
                )
                
                # Перенаправляємо на головну сторінку або категорії
                return redirect('categories:show_categories')
                
            except Exception as e:
                # Якщо виникла помилка при збереженні
                messages.error(request, f'Помилка при реєстрації: {str(e)}')
                print(f'Error during registration: {e}')  # Для debug
        else:
            # Якщо форма невалідна, показуємо помилки
            messages.error(request, 'Будь ласка, виправте помилки у формі')
    else:
        # GET запит - показуємо пусту форму
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    View для входу користувача
    """
    # Якщо користувач вже увійшов, перенаправляємо його
    if request.user.is_authenticated:
        return redirect('categories:show_categories')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        
        try:
            # Знаходимо користувача за email
            user_obj = User.objects.get(email=email)
            username = user_obj.username
            
            # Аутентифікуємо користувача
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Вхід успішний
                login(request, user)
                
                # Якщо не вибрано "Запам'ятати мене", сесія закінчиться після закриття браузера
                if not remember_me:
                    request.session.set_expiry(0)
                
                messages.success(request, f'Вітаємо, {user.first_name}! Ви успішно увійшли.')
                
                # Перенаправляємо на сторінку, з якої прийшов користувач, або на головну
                next_page = request.GET.get('next', 'categories:show_categories')
                return redirect(next_page)
            else:
                # Неправильний пароль
                messages.error(request, 'Неправильний email або пароль')
                
        except User.DoesNotExist:
            # Користувач з таким email не існує
            messages.error(request, 'Неправильний email або пароль')
        except Exception as e:
            # Інші помилки
            messages.error(request, f'Помилка при вході: {str(e)}')
            print(f'Error during login: {e}')  # Для debug
    
    return render(request, 'login.html')


def logout_view(request):
    """
    View для виходу користувача з системи
    """
    # Зберігаємо ім'я користувача для повідомлення
    user_name = request.user.first_name if request.user.first_name else request.user.username
    
    # Виходимо з системи
    logout(request)
    
    # Показуємо повідомлення
    messages.success(request, f'До побачення, {user_name}! Ви успішно вийшли з системи.')
    
    # Перенаправляємо на головну сторінку
    return redirect('/')