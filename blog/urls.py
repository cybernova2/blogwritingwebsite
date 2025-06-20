from django.urls import path
from . import views

urlpatterns = [
    # ---------- HTML Views ----------
    path('', views.index, name='index'),  # Show all posts
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # View single post
path('create/', views.create_post, name='create_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),  # Edit post
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),  # Delete post

    # ---------- API Views ----------
    path('api/posts/', views.api_get_all_posts, name='api_get_all_posts'),
    path('api/posts/<int:pk>/', views.api_get_post, name='api_get_post'),
    path('api/posts/create/', views.api_create_post, name='api_create_post'),
    path('api/posts/update/<int:pk>/', views.api_update_post, name='api_update_post'),
    path('api/posts/delete/<int:pk>/', views.api_delete_post, name='api_delete_post'),
      path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
