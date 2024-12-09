from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Patient Profile
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15, validators=[
        RegexValidator(r'^\d{10,15}$', 'Enter a valid phone number')
    ])
    email = models.EmailField()

    def __str__(self):
        return self.full_name

from django.db import models
from django.contrib.auth.models import User

DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    PMDC_no = models.CharField(max_length=20, unique=True)
    is_verified = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)

# Step 2
    speciality = models.CharField(max_length=100, default="Dermatologist")
    other_speciality = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    qualifications = models.JSONField(blank=True, null=True)  # List of degree and institute pairs
    experiences = models.JSONField(blank=True, null=True)  # List of designation and hospital pairs

    # Step 3
    city = models.CharField(max_length=100, blank=True, null=True)
    hospital_name = models.CharField(max_length=150, blank=True, null=True)
    areas_of_interest = models.JSONField(blank=True, null=True)  # List of interests
    review_address = models.TextField(blank=True, null=True)
    practice_days = models.JSONField(blank=True, null=True)  # List of selected days
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    assistant_name = models.CharField(max_length=100, blank=True, null=True)
    assistant_phone = models.CharField(max_length=15, blank=True, null=True)

    # Step 4
    online_days = models.JSONField(blank=True, null=True)  # List of selected days
    online_start_time = models.TimeField(blank=True, null=True)
    online_end_time = models.TimeField(blank=True, null=True)
    online_consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


    # Step 5
    profile_picture = models.ImageField(upload_to='doctor_pictures/', blank=True, null=True)

    def __str__(self):
        return self.full_name
