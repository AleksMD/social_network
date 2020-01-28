from rest_framework import serializers
from sn_network.models import User, Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'date_of_birth',
                  'date_of_join',
                  'like_it']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['url',
                  'author',
                  'date_of_creation',
                  'users_likes']
