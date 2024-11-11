import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import CurrentUserSerializer

class UpdateProfileImageView(APIView):
    def patch(self, request):
        user = request.user
        profile_image = request.FILES.get('profile_image')

        if not profile_image:
            return Response({"detail": "Nenhuma imagem fornecida."}, status=status.HTTP_400_BAD_REQUEST)

        # Define o caminho do diretório onde as imagens serão salvas
        profile_images_path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
        
        # Verifica se a pasta profile_images existe dentro de media; se não, cria
        if not os.path.exists(profile_images_path):
            os.makedirs(profile_images_path)

        # Atualiza o campo de imagem no usuário e salva a imagem no diretório `profile_images`
        user.profile_image.save(f"profile_images/{profile_image.name}", profile_image, save=True)

        # Retorna os dados do usuário com a nova URL da imagem
        serializer = CurrentUserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
