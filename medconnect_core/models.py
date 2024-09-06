from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save#allows us to automaticallly create a new profile when user signsup
import datetime

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    blood_type = models.CharField(max_length=2, choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS')], blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)
    allergies = models.CharField(max_length=255, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_policy_number = models.CharField(max_length=100, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    next_of_kin = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')], blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    smoking_status = models.CharField(max_length=100, blank=True, null=True)
    alcohol_consumption = models.CharField(max_length=100, blank=True, null=True)
    status= models.CharField(max_length=100, default="patient")

    def __str__(self):
        return f"{self.emergency_contact_name} ({self.phone_number})"
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile=PatientProfile(user=instance)
        user_profile.save()
#automte it
post_save.connect(create_profile, sender=User)
class Appointment(models.Model):
        patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, null=True)
        date=models.DateField(default=datetime.datetime.today)
        time = models.TimeField(default=datetime.datetime.today)
        purpose = models.TextField(max_length=100, null=True)
        doctor=models.CharField(max_length=100 , null=True)
        status = models.CharField(max_length=20, choices=[
            ('SCHEDULED', 'Scheduled'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETED', 'Completed')
        ], default='SCHEDULED')
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.purpose


class session(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    medication = models.TextField()
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return f"Prescription for {self.patient.user}"