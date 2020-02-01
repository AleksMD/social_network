from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from sn_network.utils import pretty_datetime


class UserManager(BaseUserManager):

    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Email is required')
        user = self.model(username=username,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        if not email:
            raise ValueError('Email is required')
        user = self.model(username=username,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(null=False,
                              unique=True)
    username = models.CharField(max_length=50,
                                null=False,
                                unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return f'<User: email={self.email}, username={self.username}>'


class UserProfile(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')
    email = models.EmailField(blank=False)
    date_of_join = models.DateTimeField(
        default=pretty_datetime)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return (f'<User: first name={self.first_name}, '
                f'last name={self.last_name}>')
