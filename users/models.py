from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('pro', 'Pro'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('school_admin', 'School Admin'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='learner')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # School-related fields (Phase 2)
    school = models.ForeignKey(
        'school.School', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='members'
    )
    grade = models.CharField(max_length=5, blank=True, help_text='Student grade level, e.g. 10')
    phone = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
