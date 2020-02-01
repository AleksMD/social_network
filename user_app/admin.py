from django.contrib import admin
from user_app.models import User, UserProfile


admin.register(User, UserProfile)
