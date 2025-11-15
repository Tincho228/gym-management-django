from django.contrib import admin
from .models import Instructor, Membership, Routine, Exercise, UserProfile

# Register all models
admin.site.register(Instructor)
admin.site.register(Membership)
admin.site.register(Routine)
admin.site.register(Exercise)
admin.site.register(UserProfile)