from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import User
from .tokens import first_login_token

# -----------------------------
# User Registration
# -----------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

            # Send first login email
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = first_login_token.make_token(user)
            link = reverse('first_login', kwargs={'uidb64': uid, 'token': token})
            first_login_url = f"http://{current_site.domain}{link}"

            message = f"Hi {user.username},\n\nClick the link to login for the first time:\n{first_login_url}\n\nThanks!"
            send_mail(
                'Your First Login Link',
                message,
                'Student Management <basipp123@gmail.com>',
                [user.email],
                fail_silently=False
            )

            return redirect('registration_complete')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/registration.html', {'form': form})


def registration_complete(request):
    return render(request, 'auth/reg_completed.html')


# -----------------------------
# First Login via Token
# -----------------------------
def first_login(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and first_login_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('students:student_dashboard')
    else:
        messages.error(request, "Invalid or expired link. You can resend a new first login link.")
        return redirect('resend_first_login')  # Redirect to resend page


# -----------------------------
# User Login
# -----------------------------
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                if user.role == 'Admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('students:student_dashboard')
            else:
                messages.error(request, "Your account is inactive. Please check your email.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


# -----------------------------
# User Logout
# -----------------------------
def user_logout(request):
    logout(request)
    return redirect('login')


# -----------------------------
# Resend First Login Link
# -----------------------------
def resend_first_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.info(request, "Your account is already active. Please login.")
                return redirect('login')

            # Generate new token & email
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = first_login_token.make_token(user)
            link = reverse('first_login', kwargs={'uidb64': uid, 'token': token})
            first_login_url = f"http://{current_site.domain}{link}"

            message = f"Hi {user.username},\n\nClick the link to login for the first time:\n{first_login_url}\n\nThanks!"
            send_mail(
                'Your First Login Link',
                message,
                'Student Management <basipp123@gmail.com>',
                [user.email],
                fail_silently=False
            )
            messages.success(request, "A new first login link has been sent to your email.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
    return render(request, 'auth/resend_link.html')
