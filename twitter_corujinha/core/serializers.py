from django.conf import settings
from rest_framework import serializers
from .models import User, Tweet, Comment, Follow

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
        # Contagem correta de seguidores usando Follow
        return obj.followed_relations.count()

    def get_following_count(self, obj):
        # Contagem correta de pessoas que o usuário está seguindo usando Follow
        return obj.follower_relations.count()

    def get_is_following(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # Verifica se o usuário autenticado segue o usuário atual
            return Follow.objects.filter(follower=user, followed=obj).exists()
        return False

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return settings.MEDIA_URL + obj.profile_image.name
        return None


class TweetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id', 'content', 'author', 'created_at', 'updated_at',
            'comments', 'likes_count'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    follower = serializers.ReadOnlyField(source='follower.username')
    followed = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']
