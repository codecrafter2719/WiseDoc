from django.contrib import admin
from .models import DoctorProfile

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'PMDC_no', 'is_verified', 'is_authorized']
    actions = ['mark_verified', 'mark_authorized']

    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "Selected profiles marked as verified.")

    def mark_authorized(self, request, queryset):
        queryset.update(is_authorized=True)
        self.message_user(request, "Selected profiles authorized.")
    
    mark_verified.short_description = "Mark as Verified"
    mark_authorized.short_description = "Mark as Authorized"
