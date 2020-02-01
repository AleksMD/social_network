from rest_framework import serializers
from user_app.models import UserProfile, User


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
        else:
            UserProfile.objects.create(user=user, email=user.email)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'token']
        extra_kwargs = {'password': {'write_only': True}}
