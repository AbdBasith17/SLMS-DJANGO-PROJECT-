
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landing_page(request):
    return render(request, 'students/home.html')


@login_required
def student_dashboard(request):
    context = {
        'total_courses': 5,  # Replace with real data from your DB
        'completed_courses': 2,
        'pending_assignments': 3,
        'recent_activities': [
            {'description': 'Submitted Assignment 1', 'date': '2025-10-28'},
            {'description': 'Joined Course: Python Basics', 'date': '2025-10-25'},
        ]
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def student_courses(request):
    # Replace with your actual courses queryset
    courses = []
    return render(request, 'students/courses.html', {'courses': courses})

@login_required
def student_profile(request):
    return render(request, 'students/profile.html')
