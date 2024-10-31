import logging
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer, RegisterUserSerializer

# Configuração do logger
logger = logging.getLogger(__name__)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        return UserSerializer

    def get_permissions(self):
        # Permissões flexíveis para diferentes ações do usuário
        if self.action in ['create', 'login']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f'Usuário {user.username} criado com sucesso.')

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Retorna dados do próprio usuário logado.
        Esse endpoint é utilizado para preencher o perfil do usuário no front-end.
        """
        logger.info(f'Usuário autenticado acessou o próprio perfil: {request.user.username}')
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """
        Atualiza o perfil do usuário autenticado.
        """
        user = request.user
        logger.info(f'Usuário {user.username} está tentando atualizar o perfil.')
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Perfil do usuário {user.username} atualizado com sucesso.')
            return Response({"message": "Perfil atualizado com sucesso", "data": serializer.data})

        logger.error(f'Erro ao atualizar o perfil do usuário {user.username}: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        Realiza o login do usuário e retorna tokens de acesso e dados do usuário.
        Este método facilita a autenticação de usuários para o front-end.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            logger.info(f'Usuário {username} autenticado com sucesso.')

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
            }, status=status.HTTP_200_OK)

        logger.warning(f'Tentativa de login falhou para o usuário: {username}')
        return Response(
            {"detail": "Credenciais inválidas."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def refresh_token(self, request):
        """
        Endpoint para renovar o token de acesso usando o token de atualização.
        """
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {"detail": "Token de atualização não fornecido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            logger.info(f'Token de acesso renovado para o usuário: {request.user.username}')
            return Response({
                'access': new_access_token
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Erro ao renovar token para o usuário: {request.user.username}, erro: {e}')
            return Response(
                {"detail": "Token de atualização inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )
