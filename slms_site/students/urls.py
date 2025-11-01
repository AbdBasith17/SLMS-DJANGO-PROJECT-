from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('courses/', views.student_courses, name='student_courses'),
    path('profile/', views.student_profile, name='student_profile'),
]
