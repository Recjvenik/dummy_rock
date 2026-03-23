from django.contrib import admin
from .models import SchoolInquiry


@admin.register(SchoolInquiry)
class SchoolInquiryAdmin(admin.ModelAdmin):
    list_display = ['school_name', 'contact_name', 'contact_email', 'city', 'student_count', 'interested_plan', 'submitted_at', 'is_contacted']
    list_filter = ['interested_plan', 'is_contacted', 'city']
    search_fields = ['school_name', 'contact_name', 'contact_email', 'city']
    readonly_fields = ['submitted_at']
    list_editable = ['is_contacted']
    ordering = ['-submitted_at']
    fieldsets = (
        ('School Info', {'fields': ('school_name', 'city', 'student_count', 'interested_plan')}),
        ('Contact', {'fields': ('contact_name', 'contact_email', 'contact_phone')}),
        ('Message', {'fields': ('message',)}),
        ('Follow-up', {'fields': ('is_contacted', 'notes', 'submitted_at')}),
    )
