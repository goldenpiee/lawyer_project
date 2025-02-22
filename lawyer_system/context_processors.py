def lawyer_notifications(request):
    from appointments.models import Appointment  # avoid circular imports
    if request.user.is_authenticated and hasattr(request.user, 'lawyerprofile'):
        count = Appointment.objects.filter(lawyer=request.user, status="Pending").count()
        return {'pending_appointments_count': count}
    return {}
