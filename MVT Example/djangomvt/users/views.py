from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .utils import compress_image
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                if 'image' in request.FILES:
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(300,300))
                    user.image_small.save(image_name, optimized_image, save=False)
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(800,800))
                    user.image_medium.save(image_name, optimized_image, save=False)
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(1200,1200))
                    user.image_large.save(image_name, optimized_image, save=False)
                user.save()
                messages.success(request, 'Ви успішно зареєструвалися!')
                return redirect('categories:show_categories')
            except Exception as e:
                messages.error(request, f'Помилка при реєстрації: {str(e)}')
        else:
            messages.error(request, 'Виправте помилки в формі')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    View для відображення сторінки входу
    (поки що тільки стилізація, без логіки автентифікації)
    """
    if request.method == 'POST':
        # Тут буде логіка входу пізніше
        messages.info(request, 'Функція входу ще не реалізована')
        return redirect('users:login')
    
    return render(request, 'login.html')