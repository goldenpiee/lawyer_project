from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Ожидает подтверждения'),
        ('Approved', 'Подтверждено'),
        ('Rejected', 'Отклонено'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_appointments',
        verbose_name="Клиент"
    )
    lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lawyer_appointments',
        verbose_name="Юрист"
    )
    date = models.DateTimeField(
        "Дата и время",
        help_text="Дата и время записи"
    )
    status = models.CharField(
        "Статус",
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(
        "Создано",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Обновлено",
        auto_now=True
    )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['lawyer', 'date'],
                name='unique_appointment'
            )
        ]

    def __str__(self):
        return f"{self.client.full_name} -> {self.lawyer.full_name} ({self.date})"

    def clean(self):
        if self.date < timezone.now():
            raise ValidationError("Дата записи не может быть в прошлом")
        if self.client == self.lawyer:
            raise ValidationError("Клиент и юрист не могут быть одним и тем же пользователем")

    def get_status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

class CalendarSlot(models.Model):
    lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calendar_slots',
        verbose_name="Юрист"
    )
    start_time = models.DateTimeField(
        "Начало",
        help_text="Начало временного слота"
    )
    end_time = models.DateTimeField(
        "Конец",
        help_text="Конец временного слота"
    )
    is_booked = models.BooleanField(
        "Забронирован",
        default=False
    )
    created_at = models.DateTimeField(
        "Создано",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Обновлено",
        auto_now=True
    )

    class Meta:
        verbose_name = "Временной слот"
        verbose_name_plural = "Временные слоты"
        ordering = ['start_time']
        constraints = [
            models.UniqueConstraint(
                fields=['lawyer', 'start_time'],
                name='unique_slot'
            )
        ]

    def __str__(self):
        return f"{self.lawyer.full_name} - {self.start_time}"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Время начала должно быть раньше времени окончания")
        if self.start_time < timezone.now():
            raise ValidationError("Временной слот не может быть в прошлом")