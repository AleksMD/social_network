from django.db import models
from django.utils import timezone


class User(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    date_of_join = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'<User: username={self.username}>'


class Post(models.Model):
    author = models.ForeignKey('User', related_name='author',
                               on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField(default=timezone.now)
    content = models.TextField(null=True)
    users_likes = models.ManyToManyField(User,
                                         blank=True,
                                         related_name='like_it'
                                         )

    class Meta:
        ordering = ['date_of_creation']

    def __str__(self):
        return f'<Post: post_author={self.author}>'
