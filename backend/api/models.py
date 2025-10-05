from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    SCHEDULING_CHOICES = [
        ('Atomic Habits', 'Atomic Habits'),
        ('Eisenhower Matrix', 'Eisenhower Matrix'),
        ('Time Blocking', 'Time Blocking'),
        ('Pomodoro', 'Pomodoro'),
        ('GTD', 'Getting Things Done'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    goal = models.CharField(max_length=500, help_text="User's primary goal")
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    body_fat_percentage = models.FloatField(null=True, blank=True)
    scheduling_method = models.CharField(
        max_length=50, 
        choices=SCHEDULING_CHOICES,
        default='Atomic Habits'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Objective(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='objectives')
    project = models.ForeignKey(
        Project, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='objectives'
    )
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description[:50]} - {self.date}"

    class Meta:
        ordering = ['date', '-created_at']


class DailyCheckIn(models.Model):
    MOOD_CHOICES = [
        ('Productive', 'Productive'),
        ('Tired', 'Tired'),
        ('Stressful', 'Stressful'),
        ('Energetic', 'Energetic'),
        ('Overwhelmed', 'Overwhelmed'),
        ('Focused', 'Focused'),
        ('Relaxed', 'Relaxed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_checkins')
    date = models.DateField(default=timezone.now)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.mood}"

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']


class Tip(models.Model):
    CATEGORY_CHOICES = [
        ('Quote', 'Quote'),
        ('Relaxation', 'Relaxation'),
        ('Productivity', 'Productivity'),
        ('Health', 'Health'),
        ('Mindfulness', 'Mindfulness'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    source = models.CharField(max_length=200, help_text="Author or book name")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.source}"

    class Meta:
        ordering = ['?']


class Hobby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hobbies')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=50, 
        blank=True,
        help_text="How often they engage in this hobby"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Hobbies"
