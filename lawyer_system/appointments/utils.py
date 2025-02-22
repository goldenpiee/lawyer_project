from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from accounts.models import LawyerProfile
from appointments.models import CalendarSlot
import logging

logger = logging.getLogger(__name__)

def generate_slots():
    """
    Генерирует временные слоты для записи на 30 дней вперед.
    Слоты создаются только по вторникам, средам и четвергам с 14:00 до 18:00.
    """
    try:
        lawyer_profile = LawyerProfile.objects.first()
        if not lawyer_profile:
            logger.error("Не найден профиль юриста")
            return

        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=30)
        
        logger.info(f"Начало генерации слотов с {start_date} по {end_date}")
        slots_created = 0
        
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() in [1, 2, 3]:
                logger.info(f"Обработка даты: {current_date.date()} ({current_date.weekday()})")
                start_time = current_date.replace(hour=14, minute=0)
                end_time = current_date.replace(hour=18, minute=0)
                
                while start_time < end_time:
                    slot_end = start_time + timedelta(minutes=30)
                    
                    if not CalendarSlot.objects.filter(
                        lawyer=lawyer_profile.user,
                        start_time=start_time,
                        end_time=slot_end
                    ).exists():
                        CalendarSlot.objects.create(
                            lawyer=lawyer_profile.user,
                            start_time=start_time,
                            end_time=slot_end,
                            is_booked=False
                        )
                        slots_created += 1
                    
                    start_time = slot_end
            
            current_date += timedelta(days=1)

        logger.info(f"Генерация слотов завершена. Создано слотов: {slots_created}")
        return slots_created
    
    except Exception as e:
        logger.error(f"Ошибка при генерации слотов: {str(e)}")
        return 0

def delete_old_slots():
    """
    Удаляет слоты, которые уже прошли.
    """
    CalendarSlot.objects.filter(end_time__lt=timezone.now()).delete()

def setup_slots():
    """
    Основная функция для настройки слотов.
    """
    delete_old_slots()
    generate_slots()