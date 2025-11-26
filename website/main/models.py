from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Create your models here.

class Instructor(models.Model):
    """Model for fitness instructors/personal trainers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    specialty = models.CharField(max_length=100)  # e.g., "Yoga", "Pilates", "Functional"
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialty}"

class Membership(models.Model):
    """Membership plans and user memberships"""
    PLAN_CHOICES = [
        ('basic', 'Basic Plan'),
        ('premium', 'Premium Plan'),
        ('vip', 'VIP Plan'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basic')
    start_date = models.DateField(auto_now_add=True)
    duration_days = models.IntegerField(default=30)  # 30, 90, 365 days
    is_active = models.BooleanField(default=True)
    
    @property
    def expiration_date(self):
        return self.start_date + timedelta(days=self.duration_days)
    
    @property
    def days_remaining(self):
        """Calculate days left in membership - for user dashboard"""
        if not self.is_active:
            return 0
        today = date.today()
        expiration = self.expiration_date
        days = (expiration - today).days
        return max(days, 0)  # Return 0 if expired
    
    def __str__(self):
        return f"{self.user.username} - {self.plan_type} ({self.days_remaining} days remaining)"

class Routine(models.Model):
    """Workout routines (e.g., Yoga, Pilates, Functional training)"""
    name = models.CharField(max_length=100)  # e.g., "Yoga for Beginners"
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='routines')
    duration_minutes = models.IntegerField(default=60)

    clients = models.ManyToManyField(
        'UserProfile',
        related_name='routines',
        blank=True
    )
    
    def __str__(self):
        return self.name

class Exercise(models.Model):
    """Individual exercises/classes within a routine"""
    routine = models.ForeignKey(Routine, related_name='exercises', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "Warrior Pose"
    description = models.TextField()
    repetitions = models.CharField(max_length=50, blank=True, null=True)  # e.g., "3 sets of 10"
    
    def __str__(self):
        return f"{self.name} ({self.routine.name})"

class UserProfile(models.Model):
    """Extended user profile for both admins and regular users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username