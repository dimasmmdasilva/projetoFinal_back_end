from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.user import User
from ..serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        """
        Define permissões diferentes para ações específicas.
        Permite que a criação de usuários seja feita sem autenticação,
        mas exige autenticação para todas as outras operações.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]  # Permite a criação de usuários sem autenticação
        return [permissions.IsAuthenticated()]  # Exige autenticação para as outras operações

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Retorna o perfil do usuário autenticado.
        """
        user = request.user
        serializer = self.get_serializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza a imagem de perfil e/ou biografia do usuário.
        """
        instance = self.get_object()

        # Atualiza a imagem de perfil, se fornecida
        if 'profile_image' in request.FILES:
            instance.profile_image = request.FILES.get('profile_image')

        # Atualiza a biografia, se fornecida
        if 'bio' in request.data:
            instance.bio = request.data.get('bio')

        try:
            instance.save()
            serializer = self.get_serializer(instance, context={'request': request})  # Inclui o contexto 'request' para gerar a URL completa da imagem
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
