from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

import requests
from datetime import datetime
from website import settings
from .forms import (
    CustomUserCreationForm,
    NewMembershipForm,
    RoutineForm,
    ExerciseForm,
    InstructorForm,
    AdminUserForm,
    AdminUserProfileForm,
)
from .models import Instructor, Membership, Routine, Exercise, UserProfile
from django.contrib.auth import get_user_model


# =========================
# HELPER: admin_required
# =========================

def admin_required(view_func):
    """
    Decorator to restrict views to users with UserProfile.is_admin = True
    """
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not hasattr(request.user, "profile") or not request.user.profile.is_admin:
            raise PermissionDenied("You are not allowed to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped


# =========================
# PUBLIC / AUTH VIEWS
# =========================

def home(request):
    # user information and routines
    user = request.user  # Get the current user
    role = None
    routines = None
    instructors = Instructor.objects.all()  # Show all instructors on home page

    if user.is_authenticated:
        role = "admin" if hasattr(user, "profile") and user.profile.is_admin else "client"

    # weather data
    city = 'Mendoza'  # Default city variable
    api_key = settings.OPENWEATHER_API_KEY  # OpenWeatherMap API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    weather_data = {}  # Variable to store weather data
    error_message = None

    # Calling the OpenWeatherMap API to get current weather data
    try:
        response = requests.get(url).json()
        if response.get('cod') != 200:
            error_message = response.get('message', 'Error retrieving weather data.')

        weather_data = {
            'city': response.get('name', city),
            'temperature': response.get('main', {}).get('temp'),
            'description': response.get('weather', [{}])[0].get('description'),
            'wind_speed': response.get('wind', {}).get('speed'),
            'icon': response.get('weather', [{}])[0].get('icon'),
        }
    except ValueError as e:
        error_message = str(e)

    context = {
        "user": user,
        "role": role,
        "routines": routines,
        "instructors": instructors,
        "weather_data": weather_data,
        "error_message": error_message,
    }

    return render(request, 'main/home.html', context)


@login_required
def dashboard(request):
    user = request.user
    role = "admin" if user.profile.is_admin else "client"
    routines = None
    if role == "admin" and hasattr(user, "instructor_profile"):
        routines = user.instructor_profile.routines.all()
    elif role == "client" and hasattr(user, "profile"):
        # For regular clients: show routines they are enrolled in
        routines = user.profile.routines.all()

    # Memberships info
    membership_types = Membership.PLAN_CHOICES

    # All members
    all_memberships = Membership.objects.select_related("user").all()

    # Weather
    city = 'Mendoza'
    api_key = settings.OPENWEATHER_API_KEY
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    weather_data = {}
    error_message = None

    try:
        response = requests.get(url).json()
        if response.get('cod') != 200:
            error_message = response.get('message', 'Error retrieving weather data.')

        city_name = response['city']['name']
        forecast_list = response['list']
    except ValueError as e:
        error_message = str(e)
        city_name = city
        forecast_list = []

    # Dictionary to store one forecast entry per day
    daily_forecasts = {}

    for entry in forecast_list:
        dt_object = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
        date_key = dt_object.date()
        if date_key not in daily_forecasts and len(daily_forecasts) < 5:
            daily_forecasts[date_key] = {
                'temp': entry['main']['temp'],
                'description': entry['weather'][0]['description'].capitalize(),
                'wind_speed': entry['wind']['speed'],
                'icon_code': entry['weather'][0]['icon'],
                'time_str': dt_object.strftime('%H:%M'),
                'day_name': dt_object.strftime('%A'),
            }

    context = {
        "role": role,
        "routines": routines,
        "membership_types": membership_types,
        "all_memberships": all_memberships,
        'city': city_name,
        'daily_forecasts': list(daily_forecasts.values()),
        'error_message': error_message,
    }

    return render(request, 'main/dashboard.html', context)


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "main/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('add-membership')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "main/register.html", {"form": form})


def add_membership_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if hasattr(request.user, "membership"):
        return redirect("dashboard")

    if request.method == "POST":
        form = NewMembershipForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data["plan_type"]
            duration = form.cleaned_data["duration_days"]
            Membership.objects.create(
                user=request.user,
                plan_type=plan,
                duration_days=duration
            )
            return redirect('dashboard')
    else:
        form = NewMembershipForm()

    return render(request, 'main/add-membership.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect('home')


# =========================
# ADMIN PANEL
# =========================

@admin_required
def admin_panel(request):
    """
    Simple hub page to access CRUD for instructors, routines, exercises, memberships
    """
    return render(request, "main/crud.html")


# =========================
# ROUTINE CRUD
# =========================

@admin_required
def routine_list(request):
    routines = Routine.objects.select_related('instructor').all()
    return render(request, 'main/routine_list.html', {'routines': routines})


@admin_required
def add_routine_view(request):
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Routine created successfully.")
            return redirect('routine-list')
    else:
        form = RoutineForm()
    return render(request, 'main/add-routine.html', {'form': form})


@admin_required
def edit_routine(request, id):
    routine = get_object_or_404(Routine, id=id)
    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=routine)
        if form.is_valid():
            form.save()
            messages.success(request, "Routine updated successfully.")
            return redirect('routine-list')
    else:
        form = RoutineForm(instance=routine)
    return render(request, 'main/add-routine.html', {'form': form, 'editing': True})


@admin_required
def delete_routine(request, id):
    routine = get_object_or_404(Routine, id=id)
    if request.method == 'POST':
        routine.delete()
        messages.success(request, "Routine deleted.")
        return redirect('routine-list')
    return render(request, 'main/confirm_delete.html', {'object': routine, 'type': 'Routine'})


# =========================
# EXERCISE CRUD
# =========================

@admin_required
def exercise_list(request):
    exercises = Exercise.objects.select_related('routine').all()
    return render(request, 'main/exercise_list.html', {'exercises': exercises})


@admin_required
def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exercise created successfully.")
            return redirect('exercise-list')
    else:
        form = ExerciseForm()
    return render(request, 'main/add-exercise.html', {'form': form})


@admin_required
def edit_exercise(request, id):
    exercise = get_object_or_404(Exercise, id=id)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, "Exercise updated successfully.")
            return redirect('exercise-list')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'main/add-exercise.html', {'form': form, 'editing': True})


@admin_required
def delete_exercise(request, id):
    exercise = get_object_or_404(Exercise, id=id)
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, "Exercise deleted.")
        return redirect('exercise-list')
    return render(request, 'main/confirm_delete.html', {'object': exercise, 'type': 'Exercise'})


# =========================
# INSTRUCTOR CRUD
# =========================

@admin_required
def instructor_list(request):
    instructors = Instructor.objects.select_related('user').all()
    return render(request, 'main/instructor_list.html', {'instructors': instructors})


@admin_required
def add_instructor(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor created successfully.")
            return redirect('instructor-list')
    else:
        form = InstructorForm()
    return render(request, 'main/add-instructor.html', {'form': form})


@admin_required
def edit_instructor(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    if request.method == 'POST':
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor updated successfully.")
            return redirect('instructor-list')
    else:
        form = InstructorForm(instance=instructor)
    return render(request, 'main/add-instructor.html', {'form': form, 'editing': True})


@admin_required
def delete_instructor(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    if request.method == 'POST':
        instructor.delete()
        messages.success(request, "Instructor deleted.")
        return redirect('instructor-list')
    return render(request, 'main/confirm_delete.html', {'object': instructor, 'type': 'Instructor'})

@login_required
def delete_user(request, user_id):
    if not request.user.profile.is_admin:
        return HttpResponseForbidden("Not allowed")

    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, "User deleted.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")

    return redirect('dashboard')


@admin_required
def members_list(request):
    all_memberships = Membership.objects.select_related("user").all()
    return render(request, "main/members_list.html", {
        "all_memberships": all_memberships
    })


@admin_required
def edit_user_profile(request, user_id):
    """
    Admin can edit a user's basic info + profile.
    If the UserProfile does not exist, it will be created.
    """
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = AdminUserForm(request.POST, instance=user)
        profile_form = AdminUserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "User profile saved successfully.")
            return redirect("members-list")
    else:
        user_form = AdminUserForm(instance=user)
        profile_form = AdminUserProfileForm(instance=profile)

    return render(
        request,
        "main/edit_user_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "user_obj": user,
        },
    )


##########################

@login_required
def client_routines(request):
    """Client view: browse all routines and join/leave them."""
    # If somehow an admin goes here, send them back to dashboard
    if hasattr(request.user, "profile") and request.user.profile.is_admin:
        return redirect("dashboard")

    user_profile = request.user.profile
    all_routines = (
        Routine.objects
        .select_related("instructor__user")
        .prefetch_related("exercises")
        .all()
    )

    enrolled_ids = set(
        user_profile.routines.values_list("id", flat=True)
    )

    return render(
        request,
        "main/client_routines.html",
        {
            "routines": all_routines,
            "enrolled_ids": enrolled_ids,
        },
    )


@login_required
def toggle_routine_enrollment(request, routine_id):
    """Join or leave a routine for the logged-in client."""
    if request.method != "POST":
        return redirect("client-routines")

    if hasattr(request.user, "profile") and request.user.profile.is_admin:
        return redirect("dashboard")

    profile = request.user.profile
    routine = get_object_or_404(Routine, id=routine_id)

    if profile.routines.filter(id=routine_id).exists():
        profile.routines.remove(routine)
        messages.info(request, "Routine removed from your plan.")
    else:
        profile.routines.add(routine)
        messages.success(request, "Routine added to your plan.")

    return redirect("client-routines")