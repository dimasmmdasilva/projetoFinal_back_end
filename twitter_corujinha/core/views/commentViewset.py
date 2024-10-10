from django.forms import ValidationError
from rest_framework import viewsets, permissions
from ..models.comment import Comment
from ..serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar os comentários.
    Apenas usuários autenticados podem realizar operações de criação, leitura, 
    atualização e exclusão de comentários.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna os comentários associados ao tweet.
        """
        tweet_id = self.request.query_params.get('tweet', None)
        if tweet_id:
            return Comment.objects.filter(tweet_id=tweet_id).order_by('-created_at')
        return Comment.objects.none()

    def perform_create(self, serializer):
        """
        Ao criar um comentário, associa automaticamente o autor do comentário
        ao usuário autenticado e ao tweet associado.
        """
        tweet_id = self.request.data.get('tweet')
        if tweet_id:
            serializer.save(author=self.request.user, tweet_id=tweet_id)
        else:
            raise ValidationError("Tweet ID is required to create a comment.")
