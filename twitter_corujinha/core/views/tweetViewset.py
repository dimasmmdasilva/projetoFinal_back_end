from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models.tweet import Tweet
from ..serializers import TweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna os tweets do usuário logado e dos usuários que ele segue,
        ordenados pela data de criação.
        """
        user = self.request.user
        following_ids = user.following.values_list('followed_id', flat=True)
        return Tweet.objects.filter(author__in=[user.id, *following_ids]).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def followers(self, request):
        """
        Retorna os tweets dos usuários que o usuário logado segue.
        """
        user = request.user
        following_ids = user.following.values_list('followed_id', flat=True)
        tweets_from_followers = Tweet.objects.filter(author__in=following_ids).order_by('-created_at')
        serializer = self.get_serializer(tweets_from_followers, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Cria um tweet ou uma resposta, associando o autor ao usuário logado.
        Se o tweet tiver um campo 'parent', isso indica que é uma resposta a outro tweet.
        """
        parent_tweet_id = self.request.data.get('parent', None)
        parent_tweet = None

        if parent_tweet_id:
            try:
                parent_tweet = Tweet.objects.get(id=parent_tweet_id)
            except Tweet.DoesNotExist:
                return Response(
                    {"detail": "Tweet de referência não encontrado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save(author=self.request.user, parent=parent_tweet)
