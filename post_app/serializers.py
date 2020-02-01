from rest_framework import serializers
from post_app.models import Post


class PostViewSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['url',
                  'author',
                  'title',
                  'date_of_creation',
                  'users_likes',
                  'content']
        read_only_fields = ['author', 'date_of_creation', 'users_likes']

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class PostCreateSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['title',
                  'content',
                  'author']
        read_only_fields = ['author']

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post
