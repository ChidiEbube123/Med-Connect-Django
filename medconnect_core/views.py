from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Q #for multiple queries
from django.http import JsonResponse
from django.utils import timezone

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import PatientProfile,Appointment,session, Shift
from .forms import PatientSignUpForm,PatientProfileForm, AppointmentForm,SessionForm,PatientSearchForm,ShiftForm,StaffProfileForm,StaffSignUpForm
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        profile = PatientProfile.objects.get(user__id=request.user.id)
        if profile.status!="Admin":
            return render(request, "core/index.html")
        else:
             return redirect("admin_home")
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
def admin_home(request):
    if request.user.is_authenticated:
        profile = PatientProfile.objects.get(user__id=request.user.id)
        if profile.status=="Admin":
             
            return render(request, "core/admin_index.html")
        else:
             return redirect("home")
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")

def patient_signup(request):
    if request.user.is_authenticated:
        form=PatientSignUpForm()
        if request.method=="POST":
            form=PatientSignUpForm(request.POST)
            if form.is_valid():
                
                username=form.cleaned_data["username"]
                word1=form.cleaned_data["password1"]
                word2=form.cleaned_data["password2"]
                if word1!=word2:
                    #messages.error(request, ("Please ensure that both passwords match"))
                    return redirect("patient_signup")
                form.save()
                password=form.cleaned_data["password1"]
                user=authenticate(username=username, password=password)
                use=User.objects.get(username=username)
                request.session['user_id'] = use.id
                messages.success(request,"Please enter patient profile details")
                return redirect("patient_profile", )
            else:
                messages.error(request, form.errors)
                return redirect("patient_signup")
        else:
            return render(request, "core/patient_signup.html", {"form":form})
    else:
        messages.error(request, "Please login first")
        return redirect("staff_login")
def staff_signup(request):
    if request.user.is_authenticated:
        form=StaffSignUpForm()
        if request.method=="POST":
            form=StaffSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username=form.cleaned_data["username"]
                word1=form.cleaned_data["password1"]
                word2=form.cleaned_data["password2"]
                if word1!=word2:
                    messages.success(request, ("Please ensure that both passwords match"))
                    return redirect("staff_signup")
                password=form.cleaned_data["password1"]
                user=authenticate(username=username, password=password)
                use=User.objects.get(username=username)
                request.session['user_id'] = use.id
                return redirect("staff_profile", )
            else:
                messages.error(request, form.errors)
                return redirect("patient_signup")
            return redirect("staff_signup")
        else:
            return render(request, "core/staff_signup.html", {"form":form})
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
def patient_profile(request):
     if request.user.is_authenticated:
        p=request.session.get('user_id')
        current_user_profile = PatientProfile.objects.get(user__id=p)
        form = PatientProfileForm(request.POST or None, instance=current_user_profile)
        
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Patient profile successfully updated")
                return redirect("patient_management")
            else:
                messages.error(request, "Failed to update profile. Please correct the errors below.")
                print(form.errors)  # Print form errors to the console for debugging
        
        return render(request, "core/patient_profile.html", {"form": form}) 
     else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
def staff_profile(request):
     if request.user.is_authenticated:
        p=request.session.get('user_id')
        current_user_profile = PatientProfile.objects.get(user__id=p)
        form = StaffProfileForm(request.POST or None, instance=current_user_profile)
        
        if request.method == 'POST':
            if form.is_valid():
                form.is_staff=True
                form.save()
                messages.success(request, "Staff successfully registered")
                print("dope")
                return redirect("home")
            else:
                messages.error(request, "Failed to update profile. Please correct the errors below.")
                print("noo")  # Print form errors to the console for debugging
        
        return render(request, "core/staff_profile.html", {"form": form}) 
     else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
def upload_patient(request):
    return 


def patient_management(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first")
        return redirect("staff_login")
    profile = PatientProfile.objects.get(user__id=request.user.id)
    if profile.status=="Doctor":
        return redirect("doctor_patient_management")

    patients = PatientProfile.objects.filter(is_staff=False)
    
    if request.method == "POST":
        search_query = request.POST.get('search', '')
        if search_query:
            patients = patients.filter(
                Q(user__id__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query)
            )
    p=Paginator(patients,6)
    page_number=request.GET.get('page')
    try:
        patients=p.get_page(page_number)
    except PageNotAnInteger:
        patients=p.page(1)#if pnumber isnt int assign to firstpaage
    except EmptyPage:
        patients=p.page(p.num_pages)
    
    return render(request, "core/patient_management.html", {"patients": patients})
    
def admin_patient_management(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first")
        return redirect("staff_login")
    
    patients = PatientProfile.objects.filter(is_staff=False)
    
    if request.method == "POST":
        search_query = request.POST.get('search', '')
        if search_query:
            patients = patients.filter(
                Q(user__id__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query)
            )
    p=Paginator(patients,6)
    page_number=request.GET.get('page')
    try:
        patients=p.get_page(page_number)
    except PageNotAnInteger:
        patients=p.page(1)#if pnumber isnt int assign to firstpaage
    except EmptyPage:
        patients=p.page(p.num_pages)
    
    return render(request, "core/patient_management.html", {"patients": patients})
    

def staff_management(request):
    if request.user.is_authenticated:
        staff=PatientProfile.objects.filter(is_staff=True)
        if request.method == "POST":
            search_query = request.POST.get('search', '')
            if search_query:
                staff = staff.filter(
                    Q(user__id__icontains=search_query) |
                    Q(user__first_name__icontains=search_query) |
                    Q(user__last_name__icontains=search_query)
                )
        p=Paginator(staff,6)
        page_number=request.GET.get('page')
        try:
            staff=p.get_page(page_number)
        except PageNotAnInteger:
            staff=p.page(1)#if pnumber isnt int assign to firstpaage
        except EmptyPage:
            staff=p.page(p.num_pages)
        return render(request, "core/staff_management.html", {"staff":staff
                                                              })
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")

def session_individual_view (request,id):
    if request.user.is_authenticated:
        individual_session = session.objects.get(id=id) 
        print(individual_session)
        return render(request, "core/session_individualview.html", {"session":individual_session})   
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")


def patient_view (request,id):
    if request.user.is_authenticated:
        
        appointment = Appointment.objects.filter(patient__user__id=id)  
       

        print(appointment)
        patient=PatientProfile.objects.get(user__id=id)
        sessions=session.objects.filter(patient__user__id=id)
        a=Paginator(appointment,6)  
        s=Paginator(sessions,6)  
        page_number=request.GET.get('page')#get current page
        try:
                appointment=a.get_page(page_number)#gets and returns current page
                sessions=s.get_page(page_number)#gets and returns current page
   
        except PageNotAnInteger:
                appointment=a.page(1)#if pnumber isnt int assign to firstpaage
                sessions=s.page(1)
        except EmptyPage:
                appointment=a.page(a.num_pages)
                sessions=s.page(s.num_pages)
        return render(request, "core/patient_view.html", {"patient":patient,'appointments':appointment,'sessions':sessions})
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")

def staff_view (request,id):
    if request.user.is_authenticated:

        appointments = Appointment.objects.filter(doctor__user__id=id)    
        shifts = Shift.objects.filter(staff__user__id=id)    
        staff=PatientProfile.objects.get(user__id=id)

        
        return render(request, "core/staff_view.html", {"staff":staff,"shifts":shifts,'appointments':appointments})
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")
def patient_search(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            searched = request.POST.get('searched', '')
            patients = PatientProfile.objects.filter(
                Q(user__first_name__icontains=searched) 
            )
            if patients:
                print("noo")
                return render(request, "core/patient_search.html", {'searched': patients, 'query': searched})
            else:
                messages.error(request, "No patients match your search query")
                return render(request, "patient_search.html", {'searched': None, 'query': searched})
        return render(request, "core/patient_search.html", {'searched': None, 'query': ''})
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")

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
        current_date = timezone.now().date()
        for appointment in appointments:
            if appointment.date < current_date:
                appointment.status="COMPLETED"
        if request.method == "POST":
            search_query = request.POST.get('search', '')
            if search_query:
                appointments = appointments.filter(
                    Q(patient__user__id__icontains=search_query) |
                    Q(patient__user__first_name__icontains=search_query) |
                    Q(patient__user__last_name__icontains=search_query)|
                      Q(doctor__user__first_name__icontains=search_query)|
                    Q(doctor__user__last_name__icontains=search_query)

                      
                )
        p=Paginator(appointments,6)
        page_number=request.GET.get('page')
        try:
            appointments=p.get_page(page_number)
        except PageNotAnInteger:
            appointments=p.page(1)#if pnumber isnt int assign to firstpaage
        except EmptyPage:
            appointments=p.page(p.num_pages)
    
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
    if request.user.is_authenticated:

        if request.method == 'POST':
            patient_form = PatientSearchForm(request.POST)
            session_form = SessionForm(request.POST)
            if patient_form.is_valid() :
                

                patient_id = patient_form.cleaned_data['selected_patient']
                patient = PatientProfile.objects.get(id=patient_id)
                patient_form.patient=patient
                if  session_form.is_valid():
                    #doctor=User.objects.get(id=request.user.id)
                    session = session_form.save(commit=False)
                    session.patient = patient
                    #session.doctor=doctor
                    session.save()
                    return redirect('session_view')
                else:
                    
                    print(session_form.errors)
                    print(patient_form.errors)
        else:
            print("shooop")
            patient_form = PatientSearchForm()
            session_form = SessionForm()

        return render(request, 'core/session_create.html', {
            'patient_form': patient_form,
            'session_form': session_form,
        })
    else:
            messages.success(request, "Please login first")
            return redirect("staff_login")
    

def search_patients(request):
    if request.user.is_authenticated:

        search_query = request.GET.get('q', '')
        patients = PatientProfile.objects.filter(
            Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query) | Q(id__icontains=search_query)
        )[:10]  # Limit to 10 results
        data = [{'id': p.id, 'name': p.user.first_name} for p in patients]
        return JsonResponse(data, safe=False)
    else:
            messages.success(request, "Please login first")
            return redirect("staff_login")
    
def session_view (request):
    if request.user.is_authenticated:

        sessions=session.objects.all().order_by('-time')
        p=Paginator(sessions,6)
        page_number=request.GET.get('page')
        try:
            sessions=p.get_page(page_number)
        except PageNotAnInteger:
            sessions=p.page(1)#if pnumber isnt int assign to firstpaage
        except EmptyPage:
            sessions=p.page(p.num_pages)
        
        return render(request, "core/session_view.html", {"sessions":sessions}) 
    else:
            messages.success(request, "Please login first")
            return redirect("staff_login")
    

def staff_login(request):
    if request.user.is_authenticated:

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
    else:
            messages.success(request, "Please login first")
            return redirect("staff_login")
    


def shift_view(request):
    if request.user.is_authenticated:

            shifts=Shift.objects.all()
            current_date = timezone.now().date()
            for shift in shifts:
                if shift.date < current_date:
                    shift.status="COMPLETED"
              
            if request.method == "POST":
                search_query = request.POST.get('search', '')
                if search_query:
                    shifts = shifts.filter(
                        Q(staff__user__id__icontains=search_query) |
                        Q(staff__user__first_name__icontains=search_query) |
                        Q(date__icontains=search_query)
                    )
            p=Paginator(shifts,10)
            page_number=request.GET.get('page')#get current page
            try:
                 shifts=p.get_page(page_number)#gets and returns current page
            except PageNotAnInteger:
                 shifts=p.page(1)#if pnumber isnt int assign to firstpaage
            except EmptyPage:
                 shifts=p.page(p.num_pages)#if page is empty return last page
            return render(request, "core/shift_view.html",{"shifts":shifts})
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")

def search_staff(request):
    if request.user.is_authenticated:

        search_query = request.GET.get('q', '')
        patients = PatientProfile.objects.filter(is_staff=True)
        patients = PatientProfile.objects.filter(
            Q(user__first_name__icontains=search_query) | Q(id__icontains=search_query)
        )[:10]  # Limit to 10 results
        data = [{'id': p.id, 'name': p.user.first_name} for p in patients]
        return JsonResponse(data, safe=False)
    else:
        messages.success(request, "Please login first")
        return redirect("staff_login")

def schedhule_shift (request):
    
    if request.user.is_authenticated:
                form = ShiftForm()
                if request.method == 'POST':
                    form=ShiftForm(request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Patient record successfully edited")
                        return redirect("shift_view")
                    else:
                        messages.error(request, "Failed to update profile. Please correct the errors below.")
                
                return render(request, "core/schedhule_shift.html", {"form": form}) 
    else:
            messages.success(request, "Please login first")
            return redirect("staff_login")


def staff_logout(request):
    messages.success(request, ("You have been logged out.. Thanks"))
    logout(request)
    return redirect("staff_login")
