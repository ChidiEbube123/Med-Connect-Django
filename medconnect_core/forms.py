"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StaffProfile, PatientProfile


class StaffSignupForm(UserCreationForm):
    department = forms.CharField(max_length=100)
    role = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'department', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff_member = True
        if commit:
            user.save()
            staff_profile = StaffProfile(user=user, department=self.cleaned_data['department'], role=self.cleaned_data['role'])
            staff_profile.save()
        return user

class PatientSignupForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'date_of_birth', 'gender', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
            patient_profile = PatientProfile(user=user, date_of_birth=self.cleaned_data['date_of_birth'], gender=self.cleaned_data['gender'], phone_number=self.cleaned_data['phone_number'])
            patient_profile.save()
        return user
"""

from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import PatientProfile, Appointment,session
from django import forms

class PatientSignUpForm(UserCreationForm):
    username = forms.CharField(
        label='USer Name',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )
    first_name = forms.CharField(
        label='First Name',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )
    last_name = forms.CharField(
        label='Other Names',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )
    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )
    '''
    phone = forms.CharField(
        label='Phone Number',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )
    address = forms.CharField(
        label='Address',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )'''
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )
    usable_password = None

    class Meta:
        model=User
        fields=('username','first_name', 'last_name','email')


class PatientProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded','placeholder':'2024-09-09'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    blood_type = forms.ChoiceField(choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS')], widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    emergency_contact_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    emergency_contact_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    allergies = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    medical_history = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    current_medications = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    insurance_provider = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    insurance_policy_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    additional_information = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    next_of_kin = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    marital_status = forms.ChoiceField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')], widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    occupation = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    smoking_status = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    alcohol_consumption = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}))
    class Meta:
        model=PatientProfile
        fields = (
    'date_of_birth',
    'gender',
    'blood_type',
    'phone_number',
    'address',
    'emergency_contact_name',
    'emergency_contact_number',
    'allergies',
    'medical_history',
    'current_medications',
    'insurance_provider',
    'insurance_policy_number',
    'additional_information',
    'next_of_kin',
    'marital_status',
    'occupation',
    'smoking_status',
    'alcohol_consumption'
)
class AppointmentForm(forms.ModelForm):
    purpose = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': ' Reason',
            'required': 'required',
        })
    )
    
    date = forms.DateField(
        label="Preferred Date",
        widget=forms.DateInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'type': 'date'
        })
    )
    time = forms.TimeField(
        label="Preferred Time",
        widget=forms.TimeInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'type': 'time'
        })
    )
    doctor = forms.ChoiceField(
        label="Select Doctor",
        choices=[
            ('', 'Choose a doctor'),
            ('dr-smith', 'Dr. Smith - Cardiologist'),
            ('dr-johnson', 'Dr. Johnson - Dermatologist'),
            ('dr-williams', 'Dr. Williams - Neurologist'),
        ],
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )
    status = forms.ChoiceField(
        label="Status",
        choices=[
            ('SCHEDULED', 'Scheduled'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETED', 'Completed')
        ],
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )
    class Meta:
        model=Appointment
        fields=('patient','purpose','date', 'time', 'doctor','status')
        


class PatientSearchForm(forms.Form):
    patient_search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Search by name or ID'
        })
    )
    selected_patient = forms.IntegerField(widget=forms.HiddenInput(), required=False)
class SessionForm(forms.ModelForm):
    class Meta:
        model = session
        fields = ['medication', 'dosage', 'instructions','doctor']#
        widgets = {
            'medication': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded h-32 resize-none',
                'rows': 4
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded h-32 resize-none',
                'rows': 4
            }),
        }