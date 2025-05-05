# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number must be provided')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('trainer', 'Тренер'),
        ('admin', 'Администратор'),
    ]
    
    phone = models.CharField('Телефон', max_length=15, unique=True)
    full_name = models.CharField('ФИО', max_length=255, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', max_length=1, choices=[('M', 'Мужской'), ('F', 'Женский')], blank=True)
    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES, default='client')
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Staff status', default=False)

    # Поля для тренера
    experience_years = models.PositiveIntegerField('Годы опыта', null=True, blank=True)
    achievements = models.TextField('Достижения', blank=True)

    # Поля для клиента
    goal = models.CharField('Цель тренировок', max_length=255, blank=True)
    photo = models.ImageField('Фото профиля', upload_to='profiles/', null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name or self.phone
    
    def has_perm(self, perm, obj=None):
        # Отвечает на вопрос, есть ли у пользователя конкретное право
        # Простая реализация: если это суперпользователь — всегда True
        return self.is_staff

    def has_module_perms(self, app_label):
        # Отвечает, есть ли у пользователя доступ к админ‑модулю app_label
        # Можно пускать всех staff‑пользователей:
        return self.is_staff or self.is_staff
