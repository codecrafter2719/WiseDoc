from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView

from . import views
from .views import CustomPasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('login/', LoginView.as_view(template_name='user_auth/login.html'), name='login'),  # Login URL
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Logout URL
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/doctor/step1/', views.register_doctor_step1, name='register_doctor_step1'),
    path('register/doctor/step2/', views.register_doctor_step2, name='register_doctor_step2'),
    path('register/doctor/step3/', views.register_doctor_step3, name='register_doctor_step3'),
    path('register/doctor/step4/', views.register_doctor_step4, name='register_doctor_step4'),
    path('register/doctor/step5/', views.register_doctor_step5, name='register_doctor_step5'),
    path('access/', views.access_page, name='access_page'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/patient/edit/', views.edit_patient_profile, name='edit_patient_profile'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/doctor/edit/', views.edit_doctor_profile, name='edit_doctor_profile'),
    #pass change
    path('password/change/', CustomPasswordChangeView.as_view(template_name='user_auth/change_password.html'), name='password_change'),
   



]
