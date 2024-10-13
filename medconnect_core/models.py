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
    is_staff=models.BooleanField(null=True,default=False)
    status= models.CharField(null=True, max_length=100,choices=[
        ('Patient', "Patient")  ,
          ('Doctor', "Doctor"),
          ('Admin', "Admin"),
        ('Nurse', "Nurse")
             
    ],default="Nurse", blank=True)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile=PatientProfile(user=instance)
        user_profile.save()
#automte it
post_save.connect(create_profile, sender=User)
class Appointment(models.Model):
        patient = models.ForeignKey(PatientProfile,limit_choices_to={'is_staff':False}, on_delete=models.CASCADE, null=True)
        date=models.DateField(default=datetime.datetime.today)
        time = models.TimeField(default=datetime.datetime.today)
        purpose = models.TextField(max_length=100, null=True)
        doctor=models.ForeignKey(PatientProfile,related_name="doctor" ,on_delete=models.CASCADE,limit_choices_to={'status':"Doctor"}, null=True)
        status = models.CharField(max_length=20, choices=[
            ('SCHEDULED', 'Scheduled'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETED', 'Completed')
        ], default='SCHEDULED')
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.purpose
class Time_Slot(models.Model):
     start_time = models.TimeField(default=datetime.datetime.today)
     end_time = models.TimeField(default=datetime.datetime.today)
     def __str__(self):
            return f'Slot {self.start_time} - {self.end_time} '
class Shift(models.Model):
        
        staff = models.ManyToManyField(PatientProfile,limit_choices_to={'is_staff':True}, null=True)
        date=models.DateField(default=datetime.datetime.today)
        time_slot = models.ForeignKey(Time_Slot,on_delete=models.CASCADE,null=True)

     #   doctor=models.CharField(max_length=100 , null=True)
        status = models.CharField(max_length=20, choices=[
            ('SCHEDULED', 'Scheduled'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETED', 'Completed'),
             ('ONGOING', 'Ongoing'),

        ], default='SCHEDULED')
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f'{self.date} {self.time.start_time} - {self.time.end_time}'


class session(models.Model):
    doctor = models.ForeignKey(PatientProfile,limit_choices_to={'is_staff':True}, on_delete=models.CASCADE,null=True)
    patient = models.ForeignKey(PatientProfile,related_name="patient",limit_choices_to={'is_staff':False}, on_delete=models.CASCADE, null=True, blank=True)
    notes=models.TextField(null=True)
    medication = models.TextField()
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    date=date=models.DateField(default=datetime.datetime.today)
    time=models.ForeignKey(Time_Slot, on_delete=models.CASCADE,null=True)
    # Add other fields as needed

    def __str__(self):
        return f"Prescription for {self.patient.user}"