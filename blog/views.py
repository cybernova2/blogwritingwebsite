import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import BlogPost,Category
from .forms import BlogPostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# ---------- HTML Views ----------
@login_required
def index(request):
    categories = Category.objects.all().order_by('name')  # Sort categories A-Z
    all_messages = list(messages.get_messages(request))
    if all_messages:
        last_message = all_messages[-1]
    return render(request, 'index.html', {'categories': categories,'last_message': last_message})
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
            post.author = request.user  # 🔑 Set the author properly!
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})
@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    # Check ownership
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

    # Check ownership
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('index')

    return render(request, 'delete_post.html', {'post': post})

# ---------- API Views ----------
def api_get_all_posts(request):
    posts = BlogPost.objects.all().values()
    return JsonResponse(list(posts), safe=False)

def api_get_post(request, pk):
    try:
        post = BlogPost.objects.values().get(id=pk)
        return JsonResponse(post)
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

@csrf_exempt
def api_create_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')
            
            post = BlogPost.objects.create(title=title, content=content)
            
            return JsonResponse({'id': post.id, 'title': post.title, 'content': post.content})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def api_update_post(request, pk):
    if request.method == 'POST':
        try:
            post = BlogPost.objects.get(id=pk)
            data = json.loads(request.body)
            post.title = data.get('title')
            post.content = data.get('content')
            post.save()
            return JsonResponse({'message': 'Post updated'})
        except BlogPost.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

@csrf_exempt
def api_delete_post(request, pk):
    if request.method == 'POST':
        try:
            post = BlogPost.objects.get(id=pk)
            post.delete()
            return JsonResponse({'message': 'Post deleted'})
        except BlogPost.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
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
