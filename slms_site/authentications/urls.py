from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('registration-complete/', views.registration_complete, name='registration_complete'),
    path('first-login/<uidb64>/<token>/', views.first_login, name='first_login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='auth/forgot_password.html',
        email_template_name='auth/forgot_password_email.html',
        subject_template_name='auth/forgot_password_subject.txt',
        success_url=reverse_lazy('password_reset_done')
    ), name='forgot_password'),

    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/forgot_password_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/forgot_password_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/forgot_password_complete.html'
    ), name='password_reset_complete'),
]
