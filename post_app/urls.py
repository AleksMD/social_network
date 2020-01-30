from django.urls import path
from post_app import views

urlpatterns = [
    path('posts/create_new_post', views.PostCreateView.as_view(),
         name='create_post'),
]
