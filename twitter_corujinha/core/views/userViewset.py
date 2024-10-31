import logging
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework_simplejwt.tokens import RefreshToken  # Importando RefreshToken
from ..serializers import UserSerializer, RegisterUserSerializer

logger = logging.getLogger(__name__)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f'Usuário {user.username} criado com sucesso.')

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        logger.info(f'Usuário autenticado acessou o próprio perfil: {request.user.username}')
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": _("No active account found with the given credentials.")}, 
                            status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"detail": _("No active account found with the given credentials.")}, 
                            status=status.HTTP_404_NOT_FOUND)

        # Emissão de tokens
        refresh = RefreshToken.for_user(user)
        logger.info(f'Usuário {username} autenticado com sucesso.')
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)
