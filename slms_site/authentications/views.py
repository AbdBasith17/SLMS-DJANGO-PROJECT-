from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# authentications/views.py

from .forms import UserRegisterForm, UserLoginForm

from .forms import UserRegisterForm
from .models import User
from .tokens import first_login_token





def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

           #mailllll senddinggggg 
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


# first loging usig tokennnnn checkingggg
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
        return redirect('student_dashboard')
    else:
        messages.error(request, "Invalid or expired link. Please contact support.")
        return redirect('login')


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
                    return redirect('student_dashboard')
            else:
                messages.error(request, "Your account is inactive. Please check your email.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


#loooogoutt
def user_logout(request):
    logout(request)
    return redirect('home')
