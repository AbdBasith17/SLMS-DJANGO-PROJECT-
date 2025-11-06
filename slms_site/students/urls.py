from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('profile/', views.profile, name='student_profile'),
    path('courses/', views.courses, name='student_courses'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
   
]
