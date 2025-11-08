from django.contrib.auth.decorators import user_passes_test

def admin_required(user):
    return hasattr(user, 'role') and user.role in ['Admin', 'SuperAdmin']

def superadmin_check(user):
    return hasattr(user, 'role') and user.role == 'SuperAdmin'

def student_required(user):
    return hasattr(user, 'role') and user.role == 'Student'
