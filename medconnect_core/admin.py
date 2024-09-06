from django.contrib import admin
from .models import PatientProfile,Appointment, session
# Register your models here.
admin.site.register(PatientProfile)
admin.site.register(Appointment)
admin.site.register(session)