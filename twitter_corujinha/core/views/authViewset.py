from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..serializers import UserSerializer
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            logger.info(f'Usuário {username} autenticado com sucesso.')
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user, context={'request': request}).data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": _("Nenhuma conta ativa encontrada com as credenciais fornecidas.")}, 
                            status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(f'Usuário {request.user.username} fez logout com sucesso.')
                return Response(status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                logger.error(f"Erro ao realizar logout: {str(e)}")
                return Response({"detail": "Falha ao realizar logout."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Token de refresh não fornecido."}, status=status.HTTP_400_BAD_REQUEST)
