# blog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import*

urlpatterns = [
    path('v1/posts/create/', PostCreateView.as_view(), name='post-create'),
    path('v1/posts/retrieve/', PostListView.as_view(), name='post-list-get'),
    path('v1/posts/getbyid/', PostDetailAPIView.as_view(), name='post-detail'),
    path('v1/posts/deletebyid/', PostDeleteAPIView.as_view(), name='post-delete'),
    path('v1/comment/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    

    
    # path('posts/<int:post_id>/comments/', CommentCreateAPIView.as_view(), name='add-comment'),
]