from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path('add-membership/', views.add_membership_view, name='add-membership'),
    # path('add-routine/', views.add-routine_view, name='add-routine')


     # Admin panel
    path('admin-panel/', views.admin_panel, name='admin-panel'),

    # Routines CRUD
    path('routines/', views.routine_list, name='routine-list'),
    path('routines/add/', views.add_routine_view, name='add-routine'),
    path('routines/edit/<int:id>/', views.edit_routine, name='edit-routine'),
    path('routines/delete/<int:id>/', views.delete_routine, name='delete-routine'),

    # Exercises CRUD
    path('exercises/', views.exercise_list, name='exercise-list'),
    path('exercises/add/', views.add_exercise, name='add-exercise'),
    path('exercises/edit/<int:id>/', views.edit_exercise, name='edit-exercise'),
    path('exercises/delete/<int:id>/', views.delete_exercise, name='delete-exercise'),

    # Instructors CRUD
    path('instructors/', views.instructor_list, name='instructor-list'),
    path('instructors/add/', views.add_instructor, name='add-instructor'),
    path('instructors/edit/<int:id>/', views.edit_instructor, name='edit-instructor'),
    path('instructors/delete/<int:id>/', views.delete_instructor, name='delete-instructor'),

    path('delete-user/<int:user_id>/', views.delete_user, name='delete-user'),
    path("members/", views.members_list, name="members-list"),
    path('members/<int:user_id>/edit/', views.edit_user_profile, name='edit-user-profile'),

    # Client routine selection
    path("my-routines/", views.client_routines, name="client-routines"),
    path(
        "my-routines/<int:routine_id>/toggle/",
        views.toggle_routine_enrollment,
        name="toggle-routine-enrollment",
    ),


]