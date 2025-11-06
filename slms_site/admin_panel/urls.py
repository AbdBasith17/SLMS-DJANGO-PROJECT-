from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/', views.students_list, name='students_list'),
    path('students/edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/edit/<int:course_id>/', views.course_edit, name='course_edit'),
    path('courses/delete/<int:course_id>/', views.course_delete, name='course_delete'),

    path('superadmin/', views.admin_control, name='admin_control'),
    path('superadmin/manage/', views.manage_admin, name='add_admin'),
    path('superadmin/manage/<int:admin_id>/', views.manage_admin, name='edit_admin'),
    path('superadmin/toggle/<int:admin_id>/', views.toggle_admin_status, name='toggle_admin_status'),
]
