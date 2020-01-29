from rest_framework import serializers
from sn_network.models import UserProfile, Post, User


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['url',
                  'first_name',
                  'last_name',
                  'email',
                  'date_of_birth',
                  'date_of_join',
                  'like_it']
        read_only_fields = ['date_of_join', 'like_it']


class UserSignUpSerializer(serializers.HyperlinkedModelSerializer):

    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password',
                  'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.get('profile')
        user = User.objects.create(email=validated_data['email'],
                                   username=validated_data['username'],
                                   password=validated_data['password'])
        if profile_data:
            UserProfile.objects.create(user=user,
                                       **profile_data)
        return user


class PostSerializer(serializers.HyperlinkedModelSerializer):

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
