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
from .models import PatientProfile, Appointment,session,Shift
from django import forms

class PatientSignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-field',
            "placeholder":"Patient's Username"
        }),
    )
    first_name = forms.CharField(
        label='First Name',
        required=True,
        widget=forms.TextInput(attrs={
          'class': 'form-field',
            "placeholder":"Patient's First Name"
        }),
    )
    last_name = forms.CharField(
        label='Other Names',
        required=True,
        widget=forms.TextInput(attrs={
       'class': 'form-field',
            "placeholder":"Patient's Last Name"
        }),
    )
    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={
         'class': 'form-field',
         "placeholder":"Patient's Email Address"

        }),
    )
    
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
        'class': 'form-field',
                    "placeholder":"Example aqw_135"

        }),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
          'class': 'form-field',
            "placeholder":"Confirm Password"

        }),
    )
    usable_password = None

    class Meta:
        model=User
        fields=('username','first_name', 'last_name','email')

class StaffSignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-field',
            "placeholder":"Staff's Username"
        }),
    )
    first_name = forms.CharField(
        label='First Name',
        required=True,
        widget=forms.TextInput(attrs={
          'class': 'form-field',
            "placeholder":"Staff's First Name"
        }),
    )
    last_name = forms.CharField(
        label='Other Names',
        required=True,
        widget=forms.TextInput(attrs={
       'class': 'form-field',
            "placeholder":"Staff's Last Name"
        }),
    )
    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={
         'class': 'form-field',
         "placeholder":"Staff's Email Address"

        }),
    )
    
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
        'class': 'form-field',
                    "placeholder":"Example aqw_135"

        }),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
          'class': 'form-field',
            "placeholder":"Confirm Password"

        }),
    )
    usable_password = None

    class Meta:
        model=User
        fields=('username','first_name', 'last_name','email')

class PatientProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(required=False,
   
    widget=forms.DateInput(attrs={'class': 'form-field', 'placeholder': 'YYYY-MM-DD'})
)

    gender = forms.ChoiceField(required=False,
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-field'})
    )

    blood_type = forms.ChoiceField(required=False,
        choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS')],
        widget=forms.Select(attrs={'class': 'form-field'})
    )

    phone_number = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Patient's Phone Number"})
    )

    address = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Patient's Address"})
    )

    emergency_contact_name = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Emergency Contact Name"})
    )

    emergency_contact_number = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Emergency Contact Number"})
    )

    allergies = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'class': 'form-field', "placeholder": "Known Allergies"})
    )

    medical_history = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'class': 'form-field', "placeholder": "Patient's Medical History"})
    )

    current_medications = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'class': 'form-field', "placeholder": "Current Medications"})
    )

    insurance_provider = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Insurance Provider"})
    )

    insurance_policy_number = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Insurance Policy Number"})
    )

    additional_information = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'class': 'form-field', "placeholder": "Additional Information"})
    )

    next_of_kin = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Next of Kin"})
    )

    marital_status = forms.ChoiceField(required=False,
        choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')],
        widget=forms.Select(attrs={'class': 'form-field'})
    )

    occupation = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Patient's Occupation"})
    )

    smoking_status = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Smoking Status"})
    )

    alcohol_consumption = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-field', "placeholder": "Alcohol Consumption"})
    )
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
class StaffProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(required=False,widget=forms.DateInput(attrs={ 'class': 'form-field','placeholder':'2024-09-09'}))
    gender = forms.ChoiceField(required=False,choices=[('Male', 'Male'), ('Female', 'Female')], widget=forms.Select(attrs={ 'class': 'form-field'}))
    blood_type = forms.ChoiceField(required=False,choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS')], widget=forms.Select(attrs={ 'class': 'form-field'}))
    phone_number = forms.CharField(required=False,widget=forms.TextInput(attrs={ 'class': 'form-field'}))
    address = forms.CharField(required=False,widget=forms.Textarea(attrs={ 'class': 'form-field'}))
  
    additional_information = forms.CharField(required=False,widget=forms.Textarea(attrs={ 'class': 'form-field'}))
    #is_staff=forms.BooleanField(required=False,widget=forms.CheckboxInput( attrs={'checked':'checked'}))
    status=forms.ChoiceField(required=False,label="Status", choices=[  
          ('Doctor', "Doctor"),
          ('Admin', "Admin",),
        ('Nurse', "Nurse"),
             ] , widget=forms.Select(attrs={
            'class': 'form-field'
        }))
    
    class Meta:
        model=PatientProfile
        fields = (
    'date_of_birth',
    'gender',
    'blood_type',
    'phone_number',
    'address',
    'additional_information', 
   'is_staff',
    'status',

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
        

'''   doctor = forms.ChoiceField(
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
    )'''
class PatientSearchForm(forms.Form):
    patient_search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
             'class': 'form-field',
            'placeholder': 'Search by name or ID'
        })
    )
    selected_patient = forms.IntegerField(widget=forms.HiddenInput(), required=False)
class SessionForm(forms.ModelForm):
    class Meta:
        model = session
        fields = ['notes','medication', 'dosage', 'instructions','patient','doctor', 'time']#
        widgets = {
             'notes': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded h-32 resize-none',
                'rows': 4
            }),
            'medication': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded h-32 resize-none',
                'rows': 4
            }),
            'dosage': forms.TextInput(attrs={
                 'class': 'form-field'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded h-32 resize-none',
                'rows': 4
            }),
        }

class ShiftForm(forms.ModelForm):
   
    
    date = forms.DateField(
        label="date",
        widget=forms.DateInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'type': 'date'
        })
    )

    class Meta:
        model = Shift
        fields = ['staff', 'date', 'time_slot']#
        widgets = {
            'medication': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded h-32 resize-none',
                'rows': 4
            }),
            'dosage': forms.TextInput(attrs={
                 'class': 'form-field'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded h-32 resize-none',
                'rows': 4
            }),
        }