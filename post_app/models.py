from django.db import models
from sn_network.utils import pretty_datetime
from user_app.models import UserProfile


class Post(models.Model):
    author = models.ForeignKey('user_app.User', related_name='author',
                               on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField(default=pretty_datetime)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(null=True)
    users_likes = models.ManyToManyField(UserProfile,
                                         blank=True,
                                         related_name='like_it'
                                         )

    class Meta:
        ordering = ['date_of_creation']

    def __str__(self):
        return (f'<Post: created={self.date_of_creation},'
                f'post_author={self.author}>')
