from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, Course, Enrollment
from django.contrib import messages

@login_required
def dashboard(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    enrolled_courses = Enrollment.objects.filter(student=profile)

    total_courses = enrolled_courses.count()
    completed_courses = 0  
    total_reviews = 0      
    context = {
        'profile': profile,
        'enrolled_courses': enrolled_courses,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'total_reviews': total_reviews,
    }
    return render(request, 'students/dashboard.html', context)


@login_required
def profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('students:student_profile')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'students/profile.html', {'profile': profile, 'form': form})




@login_required
def courses(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    enrolled_ids = Enrollment.objects.filter(student=profile).values_list('course_id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_ids)
    return render(request, 'students/courses.html', {'courses': available_courses})


@login_required
def enroll_course(request, course_id):
    profile = get_object_or_404(StudentProfile, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=profile, course=course)
    return redirect('students:student_dashboard')

from django.shortcuts import render, redirect
from .forms import StudentProfileForm
from django.contrib.auth.decorators import login_required

# @login_required
# def edit_profile(request):
#     profile = request.user.student_profile
#     if request.method == 'POST':
#         form = StudentProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('students:student_profile')  
#     else:
#         form = StudentProfileForm(instance=profile)
    
#     return render(request, 'students/edit_profile.html', {'form': form})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all() if hasattr(course, 'lessons') else []  # Handle missing related_name
    enrollment = Enrollment.objects.filter(course=course, student__user=request.user).first()

    return render(request, 'students/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'enrollment': enrollment,
    })
