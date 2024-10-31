from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models.tweet import Tweet
from ..serializers import TweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Tweets e suas operações associadas.
    """
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna os tweets do usuário logado e dos usuários que ele segue,
        ordenados pela data de criação mais recente.
        """
        user = self.request.user
        following_ids = user.following.values_list('followed_id', flat=True)
        return Tweet.objects.filter(author__in=[user.id, *following_ids]).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Cria um tweet ou uma resposta, associando o autor ao usuário logado.
        """
        parent_tweet_id = self.request.data.get('parent')
        parent_tweet = Tweet.objects.filter(id=parent_tweet_id).first() if parent_tweet_id else None
        serializer.save(author=self.request.user, parent=parent_tweet)

    @action(detail=False, methods=['get'])
    def followers(self, request):
        """
        Retorna os tweets dos usuários que o usuário logado segue,
        ordenados pela data de criação mais recente.
        """
        following_ids = request.user.following.values_list('followed_id', flat=True)
        tweets_from_followers = Tweet.objects.filter(author__in=following_ids).order_by('-created_at')
        serializer = self.get_serializer(tweets_from_followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        """
        Permite que o autor do tweet exclua o tweet especificado.
        """
        tweet = self.get_object()
        if tweet.author != request.user:
            return Response({"detail": "Você não tem permissão para excluir este tweet."}, status=status.HTTP_403_FORBIDDEN)

        tweet.delete()
        return Response({"detail": "Tweet excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
