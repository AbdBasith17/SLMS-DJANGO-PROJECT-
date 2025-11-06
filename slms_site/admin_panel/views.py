


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from students.models import StudentProfile, Course, Enrollment
from .forms import CourseForm, StudentEditForm, AdminForm
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()





@login_required
# @user_passes_test(admin_required)
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
# @user_passes_test(admin_required)
def students_list(request):
    students = StudentProfile.objects.filter(user__role='Student')
    return render(request, 'admin/student_list.html', {'students': students})



@login_required
# @user_passes_test(admin_required)
def student_edit(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        form = StudentEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:students_list')
        else:
            messages.error(request, form.errors)  # <-- show errors
    else:
        form = StudentEditForm(instance=student)
    return render(request, 'admin/student_edit.html', {'form': form})

@login_required
# @user_passes_test(admin_required)
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'admin/course_list.html', {'courses': courses})

@login_required
# @user_passes_test(admin_required)
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:courses_list')
    else:
        form = CourseForm()
    return render(request, 'admin/course_add.html', {'form': form})

@login_required
# @user_passes_test(admin_required)
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:courses_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin/course_edit.html', {'form': form})

@login_required
# @user_passes_test(admin_required)
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('admin_panel:courses_list')


#############################################################
#admin control

def superadmin_check(user):
    return hasattr(user, 'role') and user.role == 'SuperAdmin'


@login_required
@user_passes_test(superadmin_check)
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
def manage_admin(request, admin_id=None):
    admin_user = get_object_or_404(User, id=admin_id, role='Admin') if admin_id else None
    is_edit = bool(admin_user)

    if request.method == 'POST':
        form = AdminForm(request.POST, instance=admin_user)
        if form.is_valid():
            admin = form.save(commit=False)

            # Ensure role is always Admin
            admin.role = 'Admin'

            # If new admin, must set password
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
def toggle_admin_status(request, admin_id):
    admin_user = get_object_or_404(User, id=admin_id, role='Admin')
    admin_user.is_active = not admin_user.is_active
    admin_user.save()
    status = "activated" if admin_user.is_active else "blocked"
    messages.success(request, f"Admin '{admin_user.username}' has been {status}.")
    return redirect('admin_panel:admin_control')