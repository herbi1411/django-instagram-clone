from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Create your views here.

@require_http_methods(['POST', 'GET'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("posts:index")
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, "accounts/login.html", context)

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.profile_image = request.FILES.get("profile_image")
            print(user)
            user.save()
            auth_login(request, user)
            return redirect("posts:index")
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form' : form,
    }
    return render(request, "accounts/signup.html", context)

@require_POST
def logout(request):
    auth_logout(request)
    return redirect("accounts:login")

@require_http_methods(["POST", "GET"])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("posts:index")
    else:
        form = CustomUserChangeForm(files=request.FILES, instance=request.user)
    context = {
        "form" : form,
    }
    return render(request, "accounts/update.html", context)

@require_safe
def profile(request):
    return render(request, "accounts/profile.html")