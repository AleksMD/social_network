from user_app.models import User, UserProfile
from post_app.models import Post
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from user_app.permissions import IsOwnerOrReadOnlyUserProfile
from rest_framework.permissions import AllowAny, IsAuthenticated
from user_app.serializers import (UserProfileSerializer,
                                  UserSignUpSerializer,
                                  UserLoginSerializer)


class UserSignUpView(CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'You have been successfully registered',
            }
        return Response(response, status=status_code)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(**serializer.data).first()
        if user:
            request.user = user
        if request.user.is_authenticated:
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'You have been successfully logged in',
                }
            return Response(response, status=status_code)
        response = {
                'success': False,
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'It seems you have provided bad credentials',
                }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def user_like_post(request, post_pk=None):
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()
        post = Post.objects.filter(id=post_pk).first()
        user.user_profile.like_it.add(post)
        user.save()
        status_code = status.HTTP_200_OK
        context = [
            {'message': f'User: {user.username} likes post: {post.title}'}
        ]
        return Response(context, status_code)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def user_unlike_post(request, post_pk=None):
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()
        post = Post.objects.filter(id=post_pk).first()
        user.user_profile.like_it.remove(post)
        user.save()
        status_code = status.HTTP_200_OK
        context = [
            {'message': f'User: {user.username} unlikes post: {post.title}'}
        ]
        return Response(context, status_code)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyUserProfile]
