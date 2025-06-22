from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import BlogPost, Category
from .forms import BlogPostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# ---------- HTML Views ----------

@login_required
def index(request):
    categories = Category.objects.all().order_by('name')
    all_messages = list(messages.get_messages(request))
    last_message = all_messages[-1] if all_messages else None 
    return render(request, 'index.html', {'categories': categories, 'last_message': last_message})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('index')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('index')

    return render(request, 'delete_post.html', {'post': post})

# ---------- Auth Views ----------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')
