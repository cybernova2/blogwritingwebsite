from django.urls import path
from . import views

urlpatterns = [
    # ---------- HTML Views ----------
    path('', views.index, name='index'),  # Show all posts
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # View single post
path('create/', views.create_post, name='create_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),  # Edit post
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),  # Delete post

       
      path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
