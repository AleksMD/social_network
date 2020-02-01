from django.urls import path
from post_app import views

urlpatterns = [
    path('create_new_post/', views.PostCreateView.as_view(),
         name='create_post'),
]
