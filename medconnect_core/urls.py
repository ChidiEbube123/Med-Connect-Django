from django.urls import path
from .views import home, patient_signup,patient_search,patient_view,appointment_view,schedhule_appointment,patient_profile,staff_login,session_view,session_individual_view,session_create,patient_management,patient_edit,appointment_cancel,appointment_complete,appointment_edit,search_patients
urlpatterns = [
    path("", home, name="home"),
    path("patient_signup/", patient_signup, name="patient_signup"),
        path("patient_profile/", patient_profile, name="patient_profile"),

    path("patient_search/", patient_search, name="patient_search"),
     path("patient_management/", patient_management, name="patient_management"),
    path("patient_view/<int:id>/", patient_view, name="patient_view"),
        path("schedhule_appointment/", schedhule_appointment, name="schedhule_appointment"),
    path("appointment_view/", appointment_view, name="appointment_view"),
    path("staff_login/", staff_login, name="staff_login"),
    path("session_create/", session_create, name="session_create"),
    path("session_view/", session_view, name="session_view"),
    path("session_individual_view/", session_individual_view, name="session_individual_view"),
     path("patient_edit/<int:id>/", patient_edit, name="patient_edit"),
     path("appointment_cancel/<int:id>/", appointment_cancel, name="appointment_cancel"),
     path("appointment_complete/<int:id>/", appointment_complete, name="appointment_complete"),
      path("appointment_edit/<int:id>/", appointment_edit, name="appointment_edit"),
    path('search-patients/', search_patients, name='search_patients'),
    
]
