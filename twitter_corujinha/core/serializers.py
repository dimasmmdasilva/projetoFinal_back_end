from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from .models import User, Tweet, Comment, Follow

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        
        password_validation.validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'tweet', 'author', 'content', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'bio', 'profile_image_url',
            'followers_count', 'following_count', 'is_following'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.is_followed_by(user)
        return False

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return f"{settings.MEDIA_URL}{obj.profile_image.name}"
        return None

class CurrentUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'bio', 'profile_image_url',
            'followers_count', 'following_count'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return f"{settings.MEDIA_URL}{obj.profile_image.name}"
        return None

class TweetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Tweet
        fields = [
            'id', 'content', 'author', 'created_at', 'updated_at',
            'comments'
        ]

class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    follower = serializers.ReadOnlyField(source='follower.username')
    followed = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']
