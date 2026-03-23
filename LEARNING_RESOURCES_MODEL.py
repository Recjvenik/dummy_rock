# Add this to modules/models.py

from django.db import models

class LearningResource(models.Model):
    """External learning resources for deep dive study"""
    RESOURCE_TYPES = [
        ('video', 'Video Tutorial'),
        ('article', 'Article/Blog'),
        ('book', 'Book/eBook'),
        ('course', 'Online Course'),
        ('paper', 'Research Paper'),
        ('documentation', 'Official Documentation'),
        ('interactive', 'Interactive Tutorial'),
    ]
    
    module = models.ForeignKey('Module', related_name='resources', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='video')
    url = models.URLField(max_length=500)
    description = models.TextField(help_text='Brief description of what this resource covers')
    author = models.CharField(max_length=200, blank=True, help_text='Author/Creator name')
    duration = models.CharField(max_length=50, blank=True, help_text='e.g., "45 min", "10 hours", "300 pages"')
    difficulty = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='beginner')
    is_free = models.BooleanField(default=True)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"
