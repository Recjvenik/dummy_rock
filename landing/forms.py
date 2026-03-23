from django import forms
from .models import SchoolInquiry


class SchoolInquiryForm(forms.ModelForm):
    class Meta:
        model = SchoolInquiry
        fields = ['school_name', 'contact_name', 'contact_email', 'contact_phone', 'city', 'student_count', 'interested_plan', 'message']
        widgets = {
            'school_name': forms.TextInput(attrs={'placeholder': 'e.g. Delhi Public School, Bhopal'}),
            'contact_name': forms.TextInput(attrs={'placeholder': 'Principal / HOD name'}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'principal@school.edu.in'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': '+91 98765 43210'}),
            'city': forms.TextInput(attrs={'placeholder': 'e.g. Mumbai'}),
            'student_count': forms.NumberInput(attrs={'placeholder': 'e.g. 120', 'min': 1}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your school, grade levels, or any specific requirements...'}),
        }
