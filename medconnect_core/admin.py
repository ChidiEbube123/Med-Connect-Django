from django.contrib import admin
from .models import PatientProfile,Appointment, session,Time_Slot,Shift
# Register your models here.
admin.site.register(PatientProfile)
admin.site.register(Appointment)
admin.site.register(session),
admin.site.register(Time_Slot),
admin.site.register(Shift)