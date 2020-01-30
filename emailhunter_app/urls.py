from django.urls import path
from emailhunter_app import views

urlpatterns = [
    path('verify_email/', views.EmailVerifyView.as_view(),
         name='verify_email'),
]
