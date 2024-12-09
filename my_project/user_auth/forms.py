from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PatientProfile, DoctorProfile, DAYS_OF_WEEK

# Patient Registration Form
class PatientRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    phone_no = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone_no', 'email', 'password1', 'password2']

# Doctor Registration Forms
class DoctorStep1Form(UserCreationForm):
    full_name = forms.CharField(max_length=100, label="Full Name")
    phone_no = forms.CharField(max_length=15, label="Phone Number")
    PMDC_no = forms.CharField(max_length=20, label="PMDC Number")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_PMDC_no(self):
        PMDC_no = self.cleaned_data.get('PMDC_no')
        if DoctorProfile.objects.filter(PMDC_no=PMDC_no).exists():
            raise forms.ValidationError('A doctor with this PMDC number already exists.')
        return PMDC_no
    

class DoctorStep2Form(forms.Form):
    speciality = forms.CharField(max_length=100, initial="Dermatologist", disabled=True, label="Your Speciality")
    other_speciality = forms.CharField(max_length=100, required=False, label="Any Other Speciality")
    category = forms.ChoiceField(
        choices=[
            ('General', 'General'),
            ('Specialist', 'Specialist'),
            ('Consultant', 'Consultant'),
        ],
        label="Your Category"
    )
    qualifications = forms.JSONField(widget=forms.HiddenInput(), required=False, label="Your Qualification")  # Already JSON
    experiences = forms.JSONField(widget=forms.HiddenInput(), required=False, label="Your Experience")  # Already JSON

class DoctorStep3Form(forms.Form):
    city = forms.ChoiceField(
        choices=[
            ('City 1', 'City 1'),
            ('City 2', 'City 2'),
            ('City 3', 'City 3'),
        ],
        label="Select City"
    )
    hospital = forms.CharField(max_length=150, label="Select Hospital")
    areas_of_interest = forms.JSONField(widget=forms.HiddenInput(), required=False, label="Areas of Interest")
    review_address = forms.CharField(widget=forms.Textarea, label="Review Address")
    practice_days = forms.MultipleChoiceField(
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Select Days"
    )
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Start Time")
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="End Time")
    fee = forms.DecimalField(max_digits=8, decimal_places=2, label="Your Fee")
    assistant_name = forms.CharField(max_length=100, required=False, label="Assistant Name")
    assistant_phone = forms.CharField(max_length=15, required=False, label="Assistant Phone")


class DoctorStep4Form(forms.Form):
    online_days = forms.MultipleChoiceField(
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Select Days"
    )
    online_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Start Time")
    online_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="End Time")
    online_consultation_fee = forms.DecimalField(max_digits=8, decimal_places=2, label="Online Consultation Fee")


class DoctorStep5Form(forms.Form):
    profile_picture = forms.ImageField(
        label="Profile Picture",
        widget=forms.FileInput,
        required=True,
    )

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Validate file type
            if not picture.content_type.startswith('image'):
                raise forms.ValidationError("Only image files are allowed.")
            # Validate file size (2MB limit)
            if picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 2MB.")
        return picture


class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        exclude = ['user', 'PMDC_no']  # Exclude non-editable fields
        widgets = {
            'practice_days': forms.CheckboxSelectMultiple(choices=[
                ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
            ]),
            'online_days': forms.CheckboxSelectMultiple(choices=[
                ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
            ]),
        }

class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        exclude = ['user']