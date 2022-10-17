import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe

from accounts.models import User
from .models import Post
from .forms import CommentForm, PostForm
# Create your views here.

@require_safe
def index(request):
    posts = Post.objects.order_by("created_at")
    comment_form = CommentForm()
    context = {
        "posts" : posts,
        "comment_form" : comment_form,
    }
    return render(request, "posts/index.html", context)

@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method=="POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:index")
    else:
        form = PostForm()
    context = {
        'form' : form,
    }
    return render(request, "posts/create.html", context)

@login_required
@require_POST
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect("posts:index")

@login_required
@require_http_methods(["POST", "GET"])
def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                if request.FILES.get('image'):
                    post.image = request.FILES['image']
                post.save()
                return redirect("posts:index")
        else:
            form = PostForm(instance=post)

        context = {
            "form" : form,
            'post' : post,
        }
        return render(request, "posts/update.html", context)
    else:
        return redirect("posts:index")


@login_required
@require_POST
def comments_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    user = request.user
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = user
        comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
@require_POST
def like(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    user = request.user
    if post.like_users.filter(pk=user.pk).exists():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect("posts:index")