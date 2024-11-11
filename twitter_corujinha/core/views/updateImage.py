import os
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..serializers import CurrentUserSerializer

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

        # Define o caminho de destino para o arquivo de imagem
        media_path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
        if not os.path.exists(media_path):
            os.makedirs(media_path)  # Cria o diretório, se não existir

        # Salva a imagem diretamente na pasta 'media/profile_images/'
        user.profile_image.save(profile_image.name, profile_image, save=True)
        
        logger.debug("Imagem de perfil atualizada no banco de dados e armazenada na pasta media/profile_images.")

        # Retorna os dados do usuário com a nova URL da imagem
        serializer = CurrentUserSerializer(user, context={'request': request})
        logger.debug("Processo de upload concluído com sucesso.")
        
        return Response(serializer.data, status=status.HTTP_200_OK)
