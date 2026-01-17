from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Логін", 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть логін'
        }),
        min_length=3,
        max_length=150,
        help_text='Мінімум 3 символи. Тільки літери, цифри та @/./+/-/_'
    )
    
    email = forms.EmailField(
        label="Електронна пошта",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        }),
        help_text='Введіть дійсну електронну адресу'
    )
    
    first_name = forms.CharField(
        label="Ім'я",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть ім\'я'
        }),
        min_length=2,
        max_length=100,
        help_text='Мінімум 2 символи'
    )
    
    last_name = forms.CharField(
        label="Прізвище",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть прізвище'
        }),
        min_length=2,
        max_length=100,
        help_text='Мінімум 2 символи'
    )
    
    image = forms.ImageField(
        label="Зображення",
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Завантажте фото профілю (JPG, PNG, WEBP)'
    )
    
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль'
        }),
        help_text='Мінімум 8 символів, не тільки цифри'
    )
    
    password2 = forms.CharField(
        label="Повторіть пароль", 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторіть пароль'
        }),
        help_text='Введіть той самий пароль для підтвердження'
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'image', 'password1', 'password2')
    
    def clean_username(self):
        """Валідація логіну"""
        username = self.cleaned_data.get('username')
        
        # Перевірка мінімальної довжини
        if len(username) < 3:
            raise ValidationError('Логін має містити мінімум 3 символи')
        
        # Перевірка на допустимі символи
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError('Логін може містити тільки літери, цифри та символи @/./+/-/_')
        
        # Перевірка на унікальність
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Користувач з таким логіном вже існує')
        
        return username
    
    def clean_email(self):
        """Валідація email"""
        email = self.cleaned_data.get('email')
        
        # Перевірка на унікальність
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Ця електронна пошта вже зареєстрована')
        
        # Перевірка формату email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Введіть коректну електронну адресу')
        
        return email.lower()
    
    def clean_first_name(self):
        """Валідація імені"""
        first_name = self.cleaned_data.get('first_name')
        
        # Перевірка мінімальної довжини
        if len(first_name) < 2:
            raise ValidationError('Ім\'я має містити мінімум 2 символи')
        
        # Перевірка на літери (українські та латинські)
        if not re.match(r'^[a-zA-Zа-яА-ЯіІїЇєЄ\s\'-]+$', first_name):
            raise ValidationError('Ім\'я має містити тільки літери')
        
        return first_name.strip().title()
    
    def clean_last_name(self):
        """Валідація прізвища"""
        last_name = self.cleaned_data.get('last_name')
        
        # Перевірка мінімальної довжини
        if len(last_name) < 2:
            raise ValidationError('Прізвище має містити мінімум 2 символи')
        
        # Перевірка на літери (українські та латинські)
        if not re.match(r'^[a-zA-Zа-яА-ЯіІїЇєЄ\s\'-]+$', last_name):
            raise ValidationError('Прізвище має містити тільки літери')
        
        return last_name.strip().title()
    
    def clean_image(self):
        """Валідація зображення"""
        image = self.cleaned_data.get('image')
        
        if image:
            # Перевірка розміру файлу (максимум 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Розмір файлу не повинен перевищувати 5MB')
            
            # Перевірка типу файлу
            valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise ValidationError('Дозволені формати: JPG, PNG, WEBP')
            
            # Перевірка MIME типу
            valid_mime_types = ['image/jpeg', 'image/png', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in valid_mime_types:
                raise ValidationError('Невірний тип файлу')
        
        return image
    
    def clean_password1(self):
        """Валідація пароля"""
        password1 = self.cleaned_data.get('password1')
        
        # Перевірка мінімальної довжини
        if len(password1) < 8:
            raise ValidationError('Пароль має містити мінімум 8 символів')
        
        # Перевірка на тільки цифри
        if password1.isdigit():
            raise ValidationError('Пароль не може складатися тільки з цифр')
        
        # Перевірка на простий пароль
        common_passwords = ['12345678', 'password', 'qwerty123', '11111111']
        if password1.lower() in common_passwords:
            raise ValidationError('Цей пароль занадто простий')
        
        return password1
    
    def clean(self):
        """Загальна валідація форми"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        
        # Перевірка співпадіння паролів
        if password1 and password2 and password1 != password2:
            raise ValidationError('Паролі не співпадають')
        
        # Перевірка схожості пароля з логіном
        if password1 and username and username.lower() in password1.lower():
            raise ValidationError('Пароль не повинен містити логін')
        
        # Перевірка схожості пароля з email
        if password1 and email:
            email_name = email.split('@')[0]
            if email_name.lower() in password1.lower():
                raise ValidationError('Пароль не повинен містити частину email')
        
        return cleaned_data