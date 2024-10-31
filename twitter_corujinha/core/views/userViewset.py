import logging
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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
        if self.action == 'create':
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
