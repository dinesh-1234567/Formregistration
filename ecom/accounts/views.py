import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from base.emails import account_activation_email
from .models import Profile
# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_qs = User.objects.filter(username=username)

        if not user_qs.exists():
            messages.warning(request, 'Account Not Found')
            return HttpResponseRedirect(request.path_info)

        user = user_qs.first()


        if not hasattr(user, 'profile') or not user.profile.is_email_verified:
            messages.warning(request, 'Email Not Verified')
            return HttpResponseRedirect(request.path_info)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect("home")

        messages.warning(request, 'Invalid Credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Account Already Exists')
            return redirect('register')

        user_obj = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        profile = Profile.objects.create(
            user=user_obj,
            email_token=str(uuid.uuid4())
        )

        # account_activation_email(email, profile.email_token)  # optional
        messages.success(request, 'Account Created. Please login.')
        return redirect('login')  # e

    return render(request, 'registation.html')

def password_reset(request):
    pass
def activation_email(request,email_token):
    try:
        profile = Profile.objects.get(email_token=email_token)
        profile.is_email_verified = True
        profile.save()
        messages.success(request, 'Email Verified Successfully')
        return redirect('login')  # or wherever you want to go after activation
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid or Expired Token')
        return redirect('register')  # or show error page
    except Exception as e:
        print("Activation error:", e)
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('register')
def home(request):
    return render(request,'home.html')
def logout_user(request):
    logout(request)
    messages.success(request,'Logout Succesful')
    return redirect('home')