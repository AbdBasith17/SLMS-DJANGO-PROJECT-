from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages

from .models import StudentProfile, Course, Enrollment
from .forms import StudentProfileForm
from authentications.decorators import student_required




@login_required
@user_passes_test(student_required)
@never_cache
def dashboard(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    enrolled_courses = Enrollment.objects.filter(student=profile)

    context = {
        'profile': profile,
        'enrolled_courses': enrolled_courses,
        'total_courses': enrolled_courses.count(),
        'completed_courses': 0,
        'total_reviews': 0,
    }
    return render(request, 'students/dashboard.html', context)




@login_required
@user_passes_test(student_required)
@never_cache
def profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('students:student_profile')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'students/profile.html', {
        'profile': profile,
        'form': form
    })


#all crses

@login_required
@user_passes_test(student_required)
@never_cache
def courses(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    enrolled_ids = Enrollment.objects.filter(student=profile).values_list('course_id', flat=True)

    available_courses = Course.objects.exclude(id__in=enrolled_ids)

    return render(request, 'students/courses.html', {
        'courses': available_courses
    })


#enrol controle

@login_required
@user_passes_test(student_required)
@never_cache
def enroll_course(request, course_id):
    profile = get_object_or_404(StudentProfile, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(student=profile, course=course)

    messages.success(request, "Course enrolled successfully!")
    return redirect('students:student_dashboard')



@login_required
@user_passes_test(student_required)
@never_cache
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

   
    if course.notion_url:
        return redirect(course.notion_url)

    
    messages.warning(request, "No lessons added for this course. Please contact your mentor.")
    return redirect('students:student_dashboard')
