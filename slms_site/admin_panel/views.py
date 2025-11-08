from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth import get_user_model

from students.models import StudentProfile, Course, Enrollment
from .forms import CourseForm, StudentEditForm, AdminForm
from authentications.decorators import admin_required, superadmin_check  

User = get_user_model()

#admin side

@login_required
@user_passes_test(admin_required)
@never_cache
def dashboard(request):
    total_students = StudentProfile.objects.count()
    total_courses = Course.objects.count()
    active_enrollments = Enrollment.objects.count()
    recent_enrollments = Enrollment.objects.order_by('-id')[:5]

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'active_enrollments': active_enrollments,
        'recent_enrollments': recent_enrollments
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
@user_passes_test(admin_required)
@never_cache
def students_list(request):
    students = StudentProfile.objects.filter(user__role='Student')
    return render(request, 'admin/student_list.html', {'students': students})


@login_required
@user_passes_test(admin_required)
@never_cache
def student_edit(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        form = StudentEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student details updated successfully.")
            return redirect('admin_panel:students_list')
    else:
        form = StudentEditForm(instance=student)
    return render(request, 'admin/student_edit.html', {'form': form})


@login_required
@user_passes_test(admin_required)
@never_cache
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'admin/course_list.html', {'courses': courses})


@login_required
@user_passes_test(admin_required)
@never_cache
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect('admin_panel:courses_list')
    else:
        form = CourseForm()
    return render(request, 'admin/course_add.html', {'form': form})


@login_required
@user_passes_test(admin_required)
@never_cache
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('admin_panel:courses_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin/course_edit.html', {'form': form, 'course': course})


@login_required
@user_passes_test(admin_required)
@never_cache
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, f"Course '{course.name}' deleted successfully.")
    return redirect('admin_panel:courses_list')


#admin control for superadmin

@login_required
@user_passes_test(superadmin_check)
@never_cache
def admin_control(request):
    admins = User.objects.filter(role='Admin')
    context = {
        'admins': admins,
        'total_students': StudentProfile.objects.count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'total_admins': admins.count(),
    }
    return render(request, 'admin/admin_control.html', context)


@login_required
@user_passes_test(superadmin_check)
@never_cache
def manage_admin(request, admin_id=None):
    admin_user = get_object_or_404(User, id=admin_id, role='Admin') if admin_id else None
    is_edit = bool(admin_user)

    if request.method == 'POST':
        form = AdminForm(request.POST, instance=admin_user)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.role = 'Admin'

            if not is_edit:
                password = form.cleaned_data.get('password')
                if not password:
                    messages.error(request, "Password is required when creating a new admin.")
                    return render(request, 'admin/manage_admin.html', {'form': form, 'is_edit': is_edit})
                admin.set_password(password)

            admin.save()
            messages.success(request, "Admin updated successfully." if is_edit else "Admin created successfully.")
            return redirect('admin_panel:admin_control')
    else:
        form = AdminForm(instance=admin_user)

    return render(request, 'admin/manage_admin.html', {
        'form': form,
        'admin_user': admin_user,
        'is_edit': is_edit,
    })


@login_required
@user_passes_test(superadmin_check)
@never_cache
def toggle_admin_status(request, admin_id):
    admin_user = get_object_or_404(User, id=admin_id, role='Admin')
    admin_user.is_active = not admin_user.is_active
    admin_user.save()
    status = "activated" if admin_user.is_active else "blocked"
    messages.success(request, f"Admin '{admin_user.username}' has been {status}.")
    return redirect('admin_panel:admin_control')
