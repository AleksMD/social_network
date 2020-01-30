from django.urls import path
from user_app import views


urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup_user'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('like/user/<int:user_pk>/post/<int:post_pk>/', views.user_like_post,
         name='user_likes_it'),
    path('unlike/user/<int:user_pk>/post/<int:post_pk>/',
         views.user_unlike_post, name='user_unlikes_post')
]
