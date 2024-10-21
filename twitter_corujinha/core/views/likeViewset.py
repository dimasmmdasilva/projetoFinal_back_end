from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models.tweet import Tweet
from ..serializers import TweetSerializer

class LikeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna os tweets que o usuário autenticado curtiu.
        """
        return Tweet.objects.filter(likes=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Ação customizada para curtir um tweet.
        """
        tweet = Tweet.objects.get(pk=pk)
        user = request.user

        if tweet.likes.filter(id=user.id).exists():
            raise ValidationError("Você já curtiu este tweet.")

        tweet.likes.add(user)
        return Response({"message": "Tweet curtido com sucesso."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        """
        Ação customizada para remover uma curtida de um tweet.
        """
        tweet = Tweet.objects.get(pk=pk)
        user = request.user

        if not tweet.likes.filter(id=user.id).exists():
            return Response({"message": "Você ainda não curtiu este tweet."}, status=status.HTTP_400_BAD_REQUEST)

        tweet.likes.remove(user)
        return Response({"message": "Curtida removida com sucesso."}, status=status.HTTP_200_OK)
