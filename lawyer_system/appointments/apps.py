# appointments/apps.py
from django.apps import AppConfig

class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'

    def ready(self):
        # Импортируем здесь, чтобы избежать циклического импорта
        from .utils import generate_slots
        generate_slots()