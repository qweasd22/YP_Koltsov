from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('trainer', 'Тренер'),
        ('admin', 'Администратор'),
    ]
    phone = models.CharField('Телефон', max_length=15, unique=True)
    full_name = models.CharField('ФИО', max_length=255, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', max_length=1,
        choices=[('M','Мужской'),('F','Женский')], blank=True)
    photo = models.ImageField('Фото профиля', upload_to='profiles/', null=True, blank=True)
    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES)

    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Staff status', default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone} ({self.get_role_display()})"