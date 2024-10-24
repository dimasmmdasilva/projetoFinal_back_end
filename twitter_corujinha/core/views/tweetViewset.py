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
        ordenados pela data de criação.
        """
        following_ids = request.user.following.values_list('followed_id', flat=True)
        tweets_from_followers = Tweet.objects.filter(author__in=following_ids).order_by('-created_at')
        serializer = self.get_serializer(tweets_from_followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Adiciona uma curtida ao tweet especificado.
        """
        tweet = self.get_object()
        user = request.user

        if tweet.likes.filter(id=user.id).exists():
            return Response({"detail": "Você já curtiu este tweet."}, status=status.HTTP_400_BAD_REQUEST)

        tweet.likes.add(user)
        return Response({"detail": "Tweet curtido com sucesso.", "likes_count": tweet.likes.count()}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """
        Remove uma curtida do tweet especificado.
        """
        tweet = self.get_object()
        user = request.user

        if not tweet.likes.filter(id=user.id).exists():
            return Response({"detail": "Você ainda não curtiu este tweet."}, status=status.HTTP_400_BAD_REQUEST)

        tweet.likes.remove(user)
        return Response({"detail": "Curtida removida com sucesso.", "likes_count": tweet.likes.count()}, status=status.HTTP_200_OK)
