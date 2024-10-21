from django.conf import settings
from rest_framework import serializers
from .models import User, Tweet, Comment, Like, Follow

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    isFollowing = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_image', 'followers_count', 'following_count', 'isFollowing']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_isFollowing(self, obj):
        """
        Verifica se o usuário autenticado já está seguindo este usuário.
        """
        user = self.context['request'].user
        return obj.followers.filter(id=user.id).exists()

    def get_profile_image(self, obj):
        if obj.profile_image:
            return settings.MEDIA_URL + obj.profile_image.name
        return None

    def validate_bio(self, value):
        if len(value) > 300:
            raise serializers.ValidationError("A biografia não pode ter mais de 300 caracteres.")
        return value

    def validate_profile_image(self, value):
        if value and not value.name.lower().endswith(('png', 'jpg', 'jpeg')):
            raise serializers.ValidationError("Apenas arquivos de imagem PNG, JPG e JPEG são permitidos.")
        return value

class TweetSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = serializers.StringRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()  # Para contar likes
    is_liked_by_user = serializers.SerializerMethodField()  # Para verificar se o usuário autenticado curtiu

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'author', 'created_at', 'updated_at', 'comments', 'likes_count', 'is_liked_by_user']

    def get_likes_count(self, obj):
        # Agora contamos diretamente a relação ManyToMany de 'likes'
        return obj.likes.count()

    def get_is_liked_by_user(self, obj):
        # Verifica se o usuário autenticado já curtiu este tweet
        user = self.context['request'].user
        return obj.likes.filter(id=user.id).exists()  # Usando o ID do usuário para verificar a relação ManyToMany


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'tweet', 'author', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'tweet', 'user', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    followed = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']
