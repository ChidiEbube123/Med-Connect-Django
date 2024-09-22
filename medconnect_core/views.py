from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Q #for multiple queries
from django.http import JsonResponse

from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import PatientProfile,Appointment,session
from .forms import PatientSignUpForm,PatientProfileForm, AppointmentForm,SessionForm,PatientSearchForm
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, "core/index.html")
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")

def patient_signup(request):
    form=PatientSignUpForm()
    if request.method=="POST":
        form=PatientSignUpForm(request.POST)
        if form.is_valid():
            print("hey")
            form.save()
            username=form.cleaned_data["username"]
            word1=form.cleaned_data["password1"]
            word2=form.cleaned_data["password2"]
            if word1!=word2:
                messages.success(request, ("Please ensure that both passwords match"))
                return redirect("patient_signup")
            password=form.cleaned_data["password1"]
            user=authenticate(username=username, password=password)
            use=User.objects.get(username=username)
            request.session['user_id'] = use.id
            return redirect("patient_profile", )
        return redirect("patient_signup")
    else:
        print("dd")
        return render(request, "core/patient_signup.html", {"form":form})
def patient_profile(request):
     if request.user.is_authenticated:
        p=request.session.get('user_id')
        current_user_profile = PatientProfile.objects.get(user__id=p)
        form = PatientProfileForm(request.POST or None, instance=current_user_profile)
        
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Patient successfullyregistered")
                return redirect("home")
            else:
                messages.error(request, "Failed to update profile. Please correct the errors below.")
                print(form.errors)  # Print form errors to the console for debugging
        
        return render(request, "core/patient_profile.html", {"form": form}) 
     else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
def upload_patient(request):
    return 


def patient_management(request):
    patients=PatientProfile.objects.all()
    return render(request, "core/patient_management.html", {"patients":patients})

  
def session_individual_view (request):
    return render(request, "core/session_individualview.html")   

def patient_view (request,id):
    patient=PatientProfile.objects.get(user__id=id)

    
    return render(request, "core/patient_view.html", {"patient":patient})

def patient_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        patients = PatientProfile.objects.filter(
            Q(user__first_name__icontains=searched) 
        )
        if patients.exists():
            return render(request, "core/patient_search.html", {'searched': patients, 'query': searched})
        else:
            messages.error(request, "No patients match your search query")
            return render(request, "patient_search.html", {'searched': None, 'query': searched})
    return render(request, "core/patient_search.html", {'searched': None, 'query': ''})

def patient_edit (request,id):
    patient=PatientProfile.objects.get(user__id=id)

    if request.user.is_authenticated:
            current_user_profile = PatientProfile.objects.get(user__id=id)
            form = PatientProfileForm(request.POST or None, instance=current_user_profile)
            
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    messages.success(request, "Patient record successfully edited")
                    return redirect("home")
                else:
                    messages.error(request, "Failed to update profile. Please correct the errors below.")
                    print(form.errors)  # Print form errors to the console for debugging
            
            return render(request, "core/patient_edit.html", {"form": form}) 
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
    

def schedhule_appointment (request):
    
    if request.user.is_authenticated:
                form = AppointmentForm()
                if request.method == 'POST':
                    form=AppointmentForm(request.POST)
                    if form.is_valid():
                        print("mallek")
                        form.save()
                        messages.success(request, "Patient record successfully edited")
                        return redirect("appointment_view")
                    else:
                        messages.error(request, "Failed to update profile. Please correct the errors below.")
                        print(form.errors)  # Print form errors to the console for debugging
                
                return render(request, "core/schedhule_appointment.html", {"form": form}) 
    else:
            messages.success(request, "Please login first")
            return redirect("staff_login")

def appointment_view(request):
    if request.user.is_authenticated:

        appointments=Appointment.objects.all()
        return render(request, "core/view_appointment.html",{"appointments":appointments})
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")

def appointment_cancel(request,id):
    if request.user.is_authenticated:
        appointment = Appointment.objects.get(id=id)
        #if profile.status!="libstaff":
        #    return redirect("student_login_page")
        appointment.status="CANCELLED"
        appointment.save()
        return redirect("appointment_view")
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
 
def appointment_complete(request,id):
    if request.user.is_authenticated:
        appointment = Appointment.objects.get(id=id)
        #if profile.status!="libstaff":
        #    return redirect("student_login_page")
        appointment.status="COMPLETED"
        appointment.save()
        return redirect("appointment_view")
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
 
def appointment_edit (request,id):
    
    if request.user.is_authenticated:
                current_user_profile = Appointment.objects.get(id=id)
                form = AppointmentForm(request.POST or None, instance=current_user_profile)
                if request.method == 'POST':
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Appointment record successfully edited")
                        return redirect("appointment_view")
                    else:
                        messages.error(request, form.errors)
                
                return render(request, "core/edit_appointment.html", {"form": form, "id":id}) 
    else:
            messages.success(request, "Please login first")
            return redirect("staff_login")
    

def session_create(request):
    if request.method == 'POST':
        patient_form = PatientSearchForm(request.POST)
        session_form = SessionForm(request.POST)
        if patient_form.is_valid() and session_form.is_valid():
            

            patient_id = patient_form.cleaned_data['selected_patient']
            patient = PatientProfile.objects.get(id=patient_id)
            doctor=User.objects.get(id=request.user.id)
            print(doctor)
            session = session_form.save(commit=False)
            session.patient = patient
            session.doctor=doctor
            session.save()
            return redirect('session_view')
    else:
        patient_form = PatientSearchForm()
        session_form = SessionForm()

    return render(request, 'core/session_create.html', {
        'patient_form': patient_form,
        'session_form': session_form,
    })

def search_patients(request):
    search_query = request.GET.get('q', '')
    patients = PatientProfile.objects.filter(
        Q(user__first_name__icontains=search_query) | Q(id__icontains=search_query)
    )[:10]  # Limit to 10 results
    data = [{'id': p.id, 'name': p.user.first_name} for p in patients]
    return JsonResponse(data, safe=False)
def session_view (request):
    
    sessions=session.objects.all()

    return render(request, "core/session_view.html") 

def staff_login(request):
    if request.POST:
        username=request.POST["username"]
        password=request.POST["password"]
        
        user=authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect("home")
        else:
            messages.success(request, ("There was an error please try again"))
            return redirect("staff_login")

    return render(request, "core/staff_login.html")

def shift_view(request):
    return render(request, "core/shift_view.html")