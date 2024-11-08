from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import CurrentUserSerializer
import logging

logger = logging.getLogger(__name__)

class UpdateProfileImageView(APIView):
    def patch(self, request):
        logger.debug("Iniciando o processo de upload da imagem de perfil.")
        
        # Obtém o usuário autenticado e o arquivo de imagem enviado
        user = request.user
        profile_image = request.FILES.get('profile_image')

        if not profile_image:
            logger.error("Nenhuma imagem de perfil fornecida.")
            return Response({"detail": "Nenhuma imagem fornecida."}, status=status.HTTP_400_BAD_REQUEST)

        # Atualiza o campo de imagem do perfil
        user.profile_image = profile_image
        user.save()
        
        logger.debug("Imagem de perfil atualizada no banco de dados.")

        # Retorna os dados do usuário com a nova URL da imagem
        serializer = CurrentUserSerializer(user, context={'request': request})
        logger.debug("Processo de upload concluído com sucesso.")
        
        return Response(serializer.data, status=status.HTTP_200_OK)
