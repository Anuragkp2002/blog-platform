from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAuthorOrReadOnly,IsAuthorOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

# Create your views here.



class PostPagination(PageNumberPagination):
    page_size = 5
    
    
class PostCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        request_body=PostCreateSerializer,
        responses={
            201: PostCreateSerializer,
            400: 'Bad Request',
        },
        operation_description="Create a new post. Authentication required.",
        operation_summary="Create Post"
    )

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                'status':True,
                'message':'Post created successfully',
                'data':serializer.data
            },
            status=status.HTTP_201_CREATED)
        return Response({
            'status':False,
            'error':serializer.errors
        }, 
        status=status.HTTP_400_BAD_REQUEST)
        
        
class PostListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    
    @swagger_auto_schema(
        responses={
            200: AllPostSerializer(many=True),
            401: 'Unauthorized',
        },
        operation_description="List all posts. Authentication not required.",
        operation_summary="List Posts"
    )

    def get(self, request):
        posts = Post.objects.filter(is_deleted=False).order_by('-created_at')
        paginator = self.pagination_class()
        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = AllPostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
class PostDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('post_id', openapi.IN_QUERY, description="ID of the post to retrieve", type=openapi.TYPE_INTEGER,required=True),
            
        ],
        responses={
            200: PostSerializer,
            404: 'Not Found',
        },
        operation_description="Retrieve a post by ID. Authentication not required.",
        operation_summary="Get Post by ID"
    )

    def get(self, request):
        try:
            post_id= request.query_params.get('post_id')
            if not post_id:
                return Response({
                    'status':False,
                    'error':'Post ID is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            post = get_object_or_404(Post,id=post_id, is_deleted=False)
            serializer = PostSerializer(post)
            return Response({
                'status':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'status':False,
                'error':'Post not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
            
class PostDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('post_id', openapi.IN_QUERY, description="ID of the post to delete", type=openapi.TYPE_INTEGER,required=True),
        ],
        responses={
            204: 'No Content',
            404: 'Not Found',
        },
        operation_description="Delete a post by ID. Authentication required.",
        operation_summary="Delete Post by ID"
    )

    def delete(self, request, pk=None):
        post_id = pk or request.query_params.get('post_id')
        if not post_id:
            return Response({
                'status': False,
                'error': 'Post ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = get_object_or_404(Post,id=post_id)
            self.check_object_permissions(request, post)
            post.is_deleted = True
            post.save()
            return Response({'status': True ,'data': None}, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({
                'status': False,
                'error': 'Post not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
class CommentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=CommentCreateSerializer,
        manual_parameters=[
            openapi.Parameter('post_id', openapi.IN_QUERY, description="ID of the post to comment on", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            201: CommentCreateSerializer,
            400: 'Bad Request',
        },
        operation_description="Create a new comment on a post. Authentication required.",
        operation_summary="Create Comment"
    )

    def post(self, request):
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response({
                'status':False,
                'error':'Post ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response({
                'status':True,
                'message':'Comment created successfully',
                'data':serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status':False,
            'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)