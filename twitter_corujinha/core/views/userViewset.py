from ..models.user import User
from ..serializers import UserSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Permite criação de usuários sem autenticação para POST
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Gerar tokens de autenticação JWT
        user = User.objects.get(username=data['username'])
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

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