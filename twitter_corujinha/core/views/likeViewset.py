from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models.like import Like
from ..serializers import LikeSerializer

class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna os likes do usuário autenticado.
        """
        return Like.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Ao criar um like, verifica se o usuário já curtiu o tweet.
        """
        user = self.request.user
        tweet = serializer.validated_data['tweet']

        # Verifica se o like já existe para o tweet e o usuário
        if Like.objects.filter(user=user, tweet=tweet).exists():
            raise ValidationError("Você já curtiu este tweet.")

        # Salva o like com o usuário logado
        serializer.save(user=user)

    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        """
        Ação customizada para remover uma curtida de um tweet.
        """
        user = request.user
        like = Like.objects.filter(tweet_id=pk, user=user).first()

        if like:
            like.delete()
            return Response({"message": "Curtida removida com sucesso."})
        return Response({"message": "Você ainda não curtiu este tweet."}, status=status.HTTP_400_BAD_REQUEST)
