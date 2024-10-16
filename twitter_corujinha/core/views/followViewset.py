from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status

from ..models.follow import Follow
from ..models.user import User
from ..serializers import FollowSerializer

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow_user(self, request, pk=None):
        """
        Permite ao usuário seguir outro usuário.
        """
        followed_user = get_object_or_404(User, pk=pk)

        if request.user == followed_user:
            return Response({"message": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=followed_user
        )

        if not created:
            return Response({"message": "Você já está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"Agora você está seguindo {followed_user.username}."})

    @action(detail=True, methods=['post'])
    def unfollow_user(self, request, pk=None):
        """
        Permite ao usuário deixar de seguir outro usuário.
        """
        followed_user = get_object_or_404(User, pk=pk)

        if request.user == followed_user:
            return Response({"message": "Você não pode deixar de seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.filter(follower=request.user, followed=followed_user).first()

        if follow:
            follow.delete()
            return Response({"message": f"Você deixou de seguir {followed_user.username}."})

        return Response({"message": "Você não estava seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def following(self, request):
        """
        Lista de usuários que o usuário autenticado está seguindo.
        """
        following_users = request.user.following.all()
        serializer = self.get_serializer(following_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def followers(self, request):
        """
        Lista de usuários que seguem o usuário autenticado.
        """
        followers = request.user.followers.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)
