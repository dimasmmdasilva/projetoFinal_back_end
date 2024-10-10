from rest_framework.decorators import action
from urllib import response
from rest_framework import viewsets, permissions

from .. import serializers
from ..models.tweet import Tweet
from ..serializers import TweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna os tweets do próprio usuário logado, dos usuários que ele segue, 
        e ordena por data de criação.
        """
        user = self.request.user
        following_ids = user.following.values_list('followed_id', flat=True)
        return Tweet.objects.filter(author__in=[user.id, *following_ids]).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def followers(self, request):
        """
        Retorna tweets dos usuários que o usuário logado segue.
        """
        user = request.user
        following_ids = user.following.values_list('followed_id', flat=True)
        tweets_from_followers = Tweet.objects.filter(author__in=following_ids).order_by('-created_at')
        serializer = self.get_serializer(tweets_from_followers, many=True)
        return response(serializer.data)

    def perform_create(self, serializer):
        """
        Cria um tweet ou uma resposta, associando o autor ao usuário logado.
        Se o tweet tiver um campo 'parent', isso indica que é uma resposta a outro tweet.
        """
        parent_tweet_id = self.request.data.get('parent', None)
        parent_tweet = None

        # Verifica se o campo 'parent' foi enviado e se o tweet de referência existe
        if parent_tweet_id:
            try:
                parent_tweet = Tweet.objects.get(id=parent_tweet_id)
            except Tweet.DoesNotExist:
                raise serializers.ValidationError("Tweet de referência não encontrado.")

        # Salva o tweet, definindo o autor e o tweet 'parent' (caso exista)
        serializer.save(author=self.request.user, parent=parent_tweet)