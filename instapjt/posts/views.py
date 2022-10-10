import re
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Post
from .forms import PostForm
# Create your views here.

@require_safe
def index(request):
    posts = Post.objects.order_by("created_at")
    context = {
        "posts" : posts,
    }
    return render(request, "posts/index.html", context)

@require_http_methods(["GET", "POST"])
def create(request):
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts:index")
    else:
        form = PostForm()
    context = {
        'form' : form,
    }
    return render(request, "posts/create.html", context)

@require_POST
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect("posts:index")