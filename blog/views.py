import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BlogPost,Category
from .forms import BlogPostForm

# ---------- HTML Views ----------
def index(request):
    categories = Category.objects.all().order_by('name')  # Sort categories A-Z
    return render(request, 'index.html', {'categories': categories})
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
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
