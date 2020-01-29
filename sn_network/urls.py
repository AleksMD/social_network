"""sn_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sn_network import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


routers = DefaultRouter()
routers.register('users', views.UserProfileViewSet)
routers.register('posts', views.PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
    path('', include(routers.urls)),
    path('posts/create_new_post', views.PostCreateView.as_view(),
         name='create_post'),
    path('api/token/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.UserSignUpView.as_view(), name='signup_user'),
    path('like/user/<int:user_pk>/post/<int:post_pk>/', views.user_like_post,
         name='user_likes_it'),
    path('unlike/user/<int:user_pk>/post/<int:post_pk>/',
         views.user_unlike_post, name='user_unlikes_post')
]
