from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    WorkRegistrationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)
from .models import User, Work, PasswordResetToken

def home_view(request):
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('home')

@login_required
def dashboard_view(request):
    works = Work.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'works': works})

@login_required
def register_work_view(request):
    if request.method == 'POST':
        form = WorkRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохранение работы
            work = Work(
                author=request.user,
                title=form.cleaned_data['name'],
                description=f"Email: {form.cleaned_data['email']}\nPhone: {form.cleaned_data['phone']}\nPortfolio: {form.cleaned_data['portfolio']}",
                file=form.cleaned_data['file']
            )
            work.save()
            messages.success(request, 'Работа успешно зарегистрирована!')
            return redirect('dashboard')
    else:
        form = WorkRegistrationForm()
    return render(request, 'work_registration.html', {'form': form})

def password_reset_request_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = get_random_string(50)
                expires_at = timezone.now() + timedelta(hours=1)
                PasswordResetToken.objects.create(
                    user=user,
                    token=token,
                    expires_at=expires_at
                )
                reset_link = request.build_absolute_uri(
                    f'/reset-password/{token}/'
                )
                send_mail(
                    'Сброс пароля',
                    f'Для сброса пароля перейдите по ссылке: {reset_link}',
                    'noreply@yourdomain.com',
                    [email],
                    fail_silently=False,
                )
            messages.success(request, 'Инструкции по сбросу пароля отправлены на ваш email.')
            return redirect('login')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'sbros1.html', {'form': form})

def password_reset_confirm_view(request, token):
    reset_token = PasswordResetToken.objects.filter(token=token).first()
    if not reset_token or not reset_token.is_valid():
        messages.error(request, 'Неверная или устаревшая ссылка для сброса пароля.')
        return redirect('password_reset_request')
    
    if request.method == 'POST':
        form = CustomSetPasswordForm(reset_token.user, request.POST)
        if form.is_valid():
            form.save()
            reset_token.delete()
            messages.success(request, 'Пароль успешно изменен. Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomSetPasswordForm(reset_token.user)
    
    return render(request, 'sbros2.html', {'form': form})

def password_reset_request_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            user = User.objects.filter(email=email).first()
            if user:
                # Создаем токен для сброса пароля
                token = get_random_string(50)
                expires_at = timezone.now() + timedelta(hours=1)
                PasswordResetToken.objects.create(
                    user=user,
                    token=token,
                    expires_at=expires_at
                )
                
                # В реальном проекте здесь должна быть отправка email
                # Но для теста сразу перенаправляем на страницу сброса
                return redirect('password_reset_confirm', token=token)
            
            # Сообщение для пользователя, даже если email не найден (для безопасности)
            messages.success(request, 'Если email зарегистрирован, инструкции будут отправлены')
            return redirect('password_reset_confirm', token='demo-token')  # Для теста
    else:
        form = CustomPasswordResetForm()
    return render(request, 'sbros1.html', {'form': form})

def password_reset_confirm_view(request, token):
    # В реальном проекте проверяем токен:
    # reset_token = get_object_or_404(PasswordResetToken, token=token)
    # if not reset_token.is_valid():
    #     messages.error(request, 'Ссылка для сброса пароля недействительна или устарела')
    #     return redirect('password_reset_request')
    
    # Для демонстрации пропускаем проверку токена
    if request.method == 'POST':
        # В реальном проекте:
        # form = CustomSetPasswordForm(reset_token.user, request.POST)
        # Для демонстрации создаем временного пользователя
        User = get_user_model()
        temp_user, _ = User.objects.get_or_create(username='temp_reset_user')
        form = CustomSetPasswordForm(temp_user, request.POST)
        
        if form.is_valid():
            form.save()
            # В реальном проекте:
            # reset_token.delete()
            messages.success(request, 'Пароль успешно изменен! Теперь вы можете войти.')
            return redirect('login')
    else:
        # В реальном проекте:
        # form = CustomSetPasswordForm(reset_token.user)
        temp_user, _ = User.objects.get_or_create(username='temp_reset_user')
        form = CustomSetPasswordForm(temp_user)
    
    return render(request, 'sbros2.html', {'form': form})

@login_required
def dashboard_view(request):
    works = Work.objects.filter(author=request.user)
    return render(request, 'art/dashboard.html', {'works': works})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Work, UserActivity

@login_required
def dashboard_view(request):
    # Получаем работы пользователя
    works = Work.objects.filter(author=request.user)
    
    # Создаем контекст для шаблона
    context = {
        'works_count': works.count(),
        'favorites_count': request.user.favorites.count(),  # Предполагается наличие модели Favorite
        'orders_count': request.user.orders.count(),       # Предполагается наличие модели Order
        'recent_activities': UserActivity.objects.filter(user=request.user).order_by('-timestamp')[:5],
    }
    
    return render(request, 'art/dashboard.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Work, UserActivity

@login_required
def dashboard_view(request):
    context = {
        'works_count': Work.objects.filter(author=request.user).count(),
        'favorites_count': request.user.get_favorites_count(),
        'orders_count': request.user.get_orders_count(),
        'recent_activities': UserActivity.objects.filter(user=request.user).order_by('-timestamp')[:5],
    }
    return render(request, 'art/dashboard.html', context)