from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from accounts.models import User
from posts.forms import CommentForm
from posts.models import Post
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
            if request.FILES.get("profile_image"):
                user.profile_image = request.FILES.get("profile_image")
            user.save()
            auth_login(request, user)
            return redirect("posts:index")
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form' : form,
    }
    return render(request, "accounts/signup.html", context)

@login_required
@require_POST
def logout(request):
    auth_logout(request)
    return redirect("accounts:login")

@login_required
@require_http_methods(["POST", "GET"])
def update(request):
    if request.method == "POST":
        print(request)
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            if request.FILES.get('profile_image'):
                user.profile_image = request.FILES.get('profile_image')
            user.save()
            return redirect("accounts:profile", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form" : form,
    }
    return render(request, "accounts/update.html", context)

@require_safe
def profile(request, pk):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(author=user).order_by("created_at")
    comment_form = CommentForm()
    context = {
        "targetUser" : user,
        "posts" : posts,
        "comment_form" : comment_form,
    }
    return render(request, "accounts/profile.html", context)

@login_required
@require_POST
def follow(request, pk):
    you = User.objects.get(pk=pk)
    me = request.user
    if you.followers.filter(pk=me.pk).exists():
         you.followers.remove(me)
    else:
        you.followers.add(me)
    return redirect("accounts:profile", you.pk) 