from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

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
        Retorna os comentários associados ao tweet especificado, 
        ou todos os comentários se nenhum tweet for especificado.
        """
        tweet_id = self.request.query_params.get('tweet')
        if tweet_id:
            return Comment.objects.filter(tweet_id=tweet_id).order_by('-created_at')
        return Comment.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        """
        Cria um comentário, associando o autor ao usuário autenticado e 
        o comentário ao tweet associado.
        """
        tweet_id = self.request.data.get('tweet')
        if not tweet_id:
            raise ValidationError("O ID do tweet é necessário para criar um comentário.")
        
        serializer.save(author=self.request.user, tweet_id=tweet_id)

    @action(detail=True, methods=['delete'])
    def delete_comment(self, request, pk=None):
        """
        Ação customizada para excluir um comentário.
        """
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {"detail": "Você não tem permissão para excluir este comentário."},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response({"detail": "Comentário excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
