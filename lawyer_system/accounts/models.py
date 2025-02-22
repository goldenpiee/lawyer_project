from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not phone:
            raise ValueError('Телефон обязателен')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, phone, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        "Email",
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
                message="Некорректный формат email"
            )
        ]
    )
    full_name = models.CharField("ФИО", max_length=150)
    phone = models.CharField(
        "Телефон",
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?7?\d{10}$',
                message="Телефон должен быть в формате +7XXXXXXXXXX"
            )
        ]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class LawyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(
        "Специализация",
        max_length=100,
        choices=[
            ('BANKRUPTCY', 'Банкротство'),
            ('FAMILY', 'Семейное право'),
            ('CRIMINAL', 'Уголовное право'),
        ],
        default='BANKRUPTCY'
    )
    office_address = models.CharField(
        "Адрес офиса",
        max_length=200,
        default='г. Сегежа, ул. Ленина 19а'
    )

    def __str__(self):
        return f'Lawyer: {self.user.email}'