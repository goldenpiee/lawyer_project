from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('lawyer_dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('create/<int:slot_id>/', views.create_appointment, name='create_appointment'),
    path('slots/', views.get_slots_api, name='get_slots_api'),
    path('update-status/<int:appointment_id>/', views.update_appointment_status, name='update_status'),
    path('select_slot/', views.select_slot, name='select_slot'),
    path('delete_slot/<int:slot_id>/', views.delete_slot, name='delete_slot'),
    path('create_slot_from_day/', views.create_slot_from_day, name='create_slot_from_day'),
]
