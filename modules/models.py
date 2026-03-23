from django.db import models
from django.conf import settings


class Module(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    TAG_CHOICES = [
        ('beginner', 'Beginner'),
        ('interactive', 'Interactive'),
        ('simulator', 'Simulator'),
        ('critical', 'Critical'),
        ('deep-dive', 'Deep Dive'),
        ('advanced', 'Advanced'),
        ('sandbox', 'Sandbox'),
        ('comparison', 'Comparison'),
        ('architecture', 'Architecture'),
        ('knowledge', 'Knowledge'),
        ('foundation', 'Foundation'),
        ('practical', 'Practical'),
    ]
    GRADE_CHOICES = [
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
        ('11', 'Class 11'),
        ('12', 'Class 12'),
        ('all', 'All Grades'),
    ]

    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, default='beginner')
    icon = models.CharField(max_length=100, default='🧠')
    color = models.CharField(max_length=20, default='#00ff88')
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=True)
    estimated_time = models.PositiveIntegerField(default=30, help_text='Minutes')
    grade_level = models.CharField(max_length=5, choices=GRADE_CHOICES, default='all')
    prerequisites = models.TextField(blank=True, help_text='Prerequisite modules or knowledge')
    learning_objectives = models.TextField(blank=True, help_text='What students will learn (one per line)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Module {self.order}: {self.title}"


class Section(models.Model):
    module = models.ForeignKey(Module, related_name='sections', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    content_md = models.TextField(help_text='Markdown content for this section')
    has_visualizer = models.BooleanField(default=False)
    visualizer_type = models.CharField(max_length=50, blank=True)
    key_insight = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} > {self.title}"


class Chapter(models.Model):
    """Detailed sub-sections within a Section — theory + practical content"""
    CONTENT_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('activity', 'Activity'),
        ('experiment', 'Experiment'),
        ('example', 'Real-World Example'),
    ]
    section = models.ForeignKey(Section, related_name='chapters', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='theory')
    content_md = models.TextField(help_text='Rich markdown content')
    difficulty_level = models.CharField(max_length=20, default='beginner')
    estimated_reading_time = models.PositiveIntegerField(default=5, help_text='Minutes')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section.title} > {self.title}"


class Concept(models.Model):
    """Tags for concepts covered across modules"""
    name = models.CharField(max_length=100, unique=True)
    modules = models.ManyToManyField(Module, related_name='concepts', blank=True)

    def __str__(self):
        return self.name


class PracticalExercise(models.Model):
    """Hands-on exercises for students"""
    EXERCISE_TYPE_CHOICES = [
        ('code', 'Code Exercise'),
        ('experiment', 'Experiment'),
        ('quiz', 'Mini Quiz'),
        ('project', 'Project'),
        ('activity', 'Hands-on Activity'),
    ]
    module = models.ForeignKey(Module, related_name='exercises', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    description = models.TextField()
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPE_CHOICES, default='activity')
    instructions_md = models.TextField(help_text='Step-by-step instructions in markdown')
    starter_code = models.TextField(blank=True, help_text='Optional starter code template')
    solution_code = models.TextField(blank=True, help_text='Hidden solution code')
    hints = models.JSONField(default=list, blank=True, help_text='Progressive hints as a list')
    grade_level = models.CharField(max_length=5, default='all')
    difficulty = models.CharField(max_length=20, default='beginner')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Exercise: {self.title}"


class GlossaryTerm(models.Model):
    """AI/ML terminology with grade-appropriate definitions"""
    term = models.CharField(max_length=100, unique=True)
    definition = models.TextField(help_text='Full technical definition')
    simple_definition = models.TextField(help_text='Simple definition for class 8-10 students')
    example = models.TextField(blank=True, help_text='Real-world example')
    related_modules = models.ManyToManyField(Module, related_name='glossary_terms', blank=True)
    grade_level = models.CharField(max_length=5, default='all')
    category = models.CharField(max_length=50, blank=True, help_text='e.g. Basics, ML, DL, GenAI')

    class Meta:
        ordering = ['term']

    def __str__(self):
        return self.term


class LearningPath(models.Model):
    """Structured curriculum per grade level"""
    GRADE_CHOICES = [
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
        ('11', 'Class 11'),
        ('12', 'Class 12'),
    ]
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    modules = models.ManyToManyField(Module, related_name='learning_paths', blank=True)
    estimated_duration = models.PositiveIntegerField(default=40, help_text='Total hours')
    icon = models.CharField(max_length=10, default='📚')

    class Meta:
        ordering = ['grade']

    def __str__(self):
        return f"Class {self.grade}: {self.title}"


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='progress')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    time_spent = models.PositiveIntegerField(default=0, help_text='Seconds')
    last_accessed = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'module']

    def __str__(self):
        return f"{self.user.email} - {self.module.title}"


class QuizQuestion(models.Model):
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('truefalse', 'True/False'),
        ('code', 'Code Snippet'),
    ]
    module = models.ForeignKey(Module, related_name='quiz_questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mcq')
    question = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300, blank=True)
    option_d = models.CharField(max_length=300, blank=True)
    correct_answer = models.CharField(max_length=1, choices=[('a','A'),('b','B'),('c','C'),('d','D')])
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, default='beginner')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q: {self.question[:60]}..."


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    time_taken = models.PositiveIntegerField(help_text='Seconds')
    answers_data = models.JSONField(default=dict)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.module.title} - {self.score}%"


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
    
    module = models.ForeignKey(Module, related_name='resources', on_delete=models.CASCADE)
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
