from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from ..models.user import User
from ..models.follow import Follow
from ..serializers import UserSerializer

class FollowViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow_user(self, request, pk=None):
        followed_user = get_object_or_404(User, pk=pk)
        if request.user != followed_user:
            if not Follow.objects.filter(follower=request.user, followed=followed_user).exists():
                Follow.objects.create(follower=request.user, followed=followed_user)
                return Response({"detail": f"Agora você está seguindo {followed_user.username}.", "is_following": True}, status=status.HTTP_200_OK)
            return Response({"detail": "Você já está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unfollow_user(self, request, pk=None):
        followed_user = get_object_or_404(User, pk=pk)
        if request.user != followed_user:
            follow_instance = Follow.objects.filter(follower=request.user, followed=followed_user).first()
            if follow_instance:
                follow_instance.delete()
                return Response({"detail": f"Você deixou de seguir {followed_user.username}.", "is_following": False}, status=status.HTTP_200_OK)
            return Response({"detail": "Você não está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Você não pode deixar de seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def following(self, request):
        following_users = request.user.following.all()
        serializer = UserSerializer(following_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def followers(self, request):
        followers = request.user.followers.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)