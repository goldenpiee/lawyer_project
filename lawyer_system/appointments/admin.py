from django.contrib import admin
from .models import Appointment, CalendarSlot

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'lawyer', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('client__full_name', 'lawyer__full_name')

admin.site.register(Appointment, AppointmentAdmin)

class CalendarSlotAdmin(admin.ModelAdmin):
    list_display = ('lawyer', 'start_time', 'end_time', 'is_booked')
    list_filter = ('is_booked', 'start_time')
    date_hierarchy = 'start_time'

admin.site.register(CalendarSlot, CalendarSlotAdmin)