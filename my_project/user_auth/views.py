from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import (
    PatientRegistrationForm, DoctorStep1Form, DoctorStep2Form, DoctorStep3Form, DoctorStep4Form, DoctorStep5Form,
    DoctorProfileUpdateForm,PatientProfileUpdateForm
)
from .models import DoctorProfile, PatientProfile
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
import json
from django.contrib.auth.views import PasswordChangeView


def home(request):
    return render(request, 'user_auth/home.html')

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            PatientProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone_no=form.cleaned_data['phone_no'],
                email=form.cleaned_data['email']
            )
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'user_auth/register_patient.html', {'form': form})

def register_doctor_step1(request):
    if request.method == 'POST':
        form = DoctorStep1Form(request.POST)
        if form.is_valid():
            try:
                # Create the user
                user = form.save()

                # Validate and create the associated DoctorProfile
                DoctorProfile.objects.create(
                    user=user,
                    full_name=form.cleaned_data['full_name'],
                    phone_no=form.cleaned_data['phone_no'],
                    email=form.cleaned_data['email'],
                    PMDC_no=form.cleaned_data['PMDC_no'],
                )

                # Store the user ID in the session for subsequent steps
                request.session['doctor_user_id'] = user.id

                return redirect('register_doctor_step2')
            except IntegrityError:
                form.add_error('PMDC_no', 'A doctor with this PMDC number already exists.')
    else:
        form = DoctorStep1Form()
    return render(request, 'user_auth/register_doctor_step1.html', {'form': form})


def register_doctor_step2(request):
    doctor = get_object_or_404(DoctorProfile, user_id=request.session['doctor_user_id'])
    if request.method == 'POST':
        form = DoctorStep2Form(request.POST)
        if form.is_valid():
            doctor.other_speciality = form.cleaned_data['other_speciality']
            doctor.category = form.cleaned_data['category']
            doctor.qualifications = form.cleaned_data['qualifications']  # Already a list
            doctor.experiences = form.cleaned_data['experiences']  # Already a list
            doctor.save()
            return redirect('register_doctor_step3')
    else:
        form = DoctorStep2Form()
    return render(request, 'user_auth/register_doctor_step2.html', {'form': form})

def register_doctor_step3(request):
    doctor = get_object_or_404(DoctorProfile, user_id=request.session['doctor_user_id'])
    if request.method == 'POST':
        form = DoctorStep3Form(request.POST)
        if form.is_valid():
            doctor.city = form.cleaned_data['city']
            doctor.hospital_name = form.cleaned_data['hospital']
            doctor.areas_of_interest = form.cleaned_data['areas_of_interest']  # Already JSON-compatible
            doctor.review_address = form.cleaned_data['review_address']
            doctor.practice_days = form.cleaned_data['practice_days']  # Already JSON-compatible
            doctor.start_time = form.cleaned_data['start_time']
            doctor.end_time = form.cleaned_data['end_time']
            doctor.fee = form.cleaned_data['fee']
            doctor.assistant_name = form.cleaned_data.get('assistant_name')
            doctor.assistant_phone = form.cleaned_data.get('assistant_phone')
            doctor.save()
            return redirect('register_doctor_step4')
    else:
        form = DoctorStep3Form()
    return render(request, 'user_auth/register_doctor_step3.html', {'form': form})


def register_doctor_step4(request):
    doctor = get_object_or_404(DoctorProfile, user_id=request.session['doctor_user_id'])
    if request.method == 'POST':
        form = DoctorStep4Form(request.POST)
        if form.is_valid():
            doctor.online_days = form.cleaned_data['online_days']
            doctor.online_start_time = form.cleaned_data['online_start_time']
            doctor.online_end_time = form.cleaned_data['online_end_time']
            doctor.online_consultation_fee = form.cleaned_data['online_consultation_fee']
            if doctor.online_start_time >= doctor.online_end_time:
                form.add_error('online_end_time', 'End time must be after start time.')
                print("Validation error: End time must be after start time.")  # Debugging log
            else:
                doctor.save()
                print("Step 4 completed successfully. Redirecting to Step 5.")  # Debugging log
                return redirect('register_doctor_step5')
        else:
            print("Form is invalid:", form.errors)  # Debugging log
    else:
        form = DoctorStep4Form()
    return render(request, 'user_auth/register_doctor_step4.html', {'form': form})


def register_doctor_step5(request):
    doctor = get_object_or_404(DoctorProfile, user_id=request.session['doctor_user_id'])
    if request.method == 'POST':
        form = DoctorStep5Form(request.POST, request.FILES)
        if form.is_valid():
            doctor.profile_picture = form.cleaned_data['profile_picture']
            doctor.save()
            request.session.pop('doctor_user_id', None)  # Clear session after registration
            return redirect('login')  # Redirect to login after registration
    else:
        form = DoctorStep5Form()
    return render(request, 'user_auth/register_doctor_step5.html', {'form': form})

# Similarly implement `register_doctor_step3`, `register_doctor_step4`, `register_doctor_step5`

@login_required
def dashboard(request):
    if hasattr(request.user, 'patientprofile'):
        return render(request, 'user_auth/patient_dashboard.html', {'profile': request.user.patientprofile})
    elif hasattr(request.user, 'doctorprofile'):
        doctor = request.user.doctorprofile
        if not doctor.is_verified:
            return render(request, 'user_auth/verification_pending.html')
        return render(request, 'user_auth/doctor_dashboard.html', {'profile': doctor})




@login_required
def access_page(request):
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
        if not doctor.is_verified:
            return render(request, 'user_auth/verification_pending.html', {
                'message': "Your profile is under PMDC verification."
            })
        if not doctor.is_authorized:
            return render(request, 'user_auth/verification_pending.html', {
                'message': "Your profile is pending admin authorization."
            })
        return redirect('doctor_dashboard')
    except DoctorProfile.DoesNotExist:
        return redirect('home')
    

@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctorprofile
    except AttributeError:
        return render(request, 'user_auth/error.html', {'message': "Profile not found!"})

    return render(request, 'user_auth/doctor_dashboard.html', {'doctor': doctor})



@login_required
def edit_doctor_profile(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    if request.method == 'POST':
        form = DoctorProfileUpdateForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  # Redirect to dashboard after saving
    else:
        form = DoctorProfileUpdateForm(instance=doctor)
    return render(request, 'user_auth/edit_doctor_profile.html', {'form': form})


def login_redirect(request):
    try:
        if hasattr(request.user, 'patientprofile'):
            return redirect('patient_dashboard')
        elif hasattr(request.user, 'doctorprofile'):
            return redirect('access_page')
        else:
            return redirect('home')
    except Exception:
        return redirect('home')


@login_required
def patient_dashboard(request):
    # Assuming there's a PatientProfile model linked to the user
    try:
        profile = request.user.patientprofile  # Ensure the user has a PatientProfile
    except AttributeError:
        return render(request, 'user_auth/error.html', {'message': "Profile not found!"})

    # Pass the patient's profile to the dashboard template
    return render(request, 'user_auth/patient_dashboard.html', {'profile': profile})

@login_required
def edit_patient_profile(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = PatientProfileUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')  # Redirect to dashboard after saving
    else:
        form = PatientProfileUpdateForm(instance=patient)
    return render(request, 'user_auth/edit_patient_profile.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'doctorprofile'):
            return '/dashboard/doctor/'  # Redirect to doctor dashboard
        elif hasattr(user, 'patientprofile'):
            return '/dashboard/patient/'  # Redirect to patient dashboard
        else:
            return '/'  # Default fallback (e.g., home page)
