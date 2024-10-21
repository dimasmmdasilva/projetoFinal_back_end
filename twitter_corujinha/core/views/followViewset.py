from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status

from ..models.user import User
from ..serializers import UserSerializer

class FollowViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow_user(self, request, pk=None):
        """
        Permite ao usuário seguir outro usuário.
        """
        followed_user = get_object_or_404(User, pk=pk)

        if request.user == followed_user:
            return Response({"message": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.following.filter(id=followed_user.id).exists():
            request.user.following.add(followed_user)
            return Response({"message": f"Agora você está seguindo {followed_user.username}."}, status=status.HTTP_200_OK)
        return Response({"message": "Você já está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unfollow_user(self, request, pk=None):
        """
        Permite ao usuário deixar de seguir outro usuário.
        """
        followed_user = get_object_or_404(User, pk=pk)

        if request.user == followed_user:
            return Response({"message": "Você não pode deixar de seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.following.filter(id=followed_user.id).exists():
            request.user.following.remove(followed_user)
            return Response({"message": f"Você deixou de seguir {followed_user.username}."}, status=status.HTTP_200_OK)
        return Response({"message": "Você não está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def following(self, request):
        """
        Lista de usuários que o usuário autenticado está seguindo.
        """
        following_users = request.user.following.all()
        serializer = UserSerializer(following_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def followers(self, request):
        """
        Lista de usuários que seguem o usuário autenticado.
        """
        followers = request.user.followers.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)
