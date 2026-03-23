from django.db import models


class SchoolInquiry(models.Model):
    PLAN_CHOICES = [
        ('school_annual', 'School Annual — ₹15,000/yr'),
        ('school_monthly', 'School Monthly — ₹1,500/mo'),
        ('demo', 'Request Free Demo'),
    ]
    school_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    student_count = models.PositiveIntegerField()
    interested_plan = models.CharField(max_length=30, choices=PLAN_CHOICES)
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'School Inquiry'
        verbose_name_plural = 'School Inquiries'

    def __str__(self):
        return f"{self.school_name} — {self.contact_name} ({self.submitted_at.date()})"
