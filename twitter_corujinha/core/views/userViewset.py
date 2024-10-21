from ..models.user import User
from ..serializers import UserSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()  # Certifica-se de que está usando o modelo de usuário customizado

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        """
        Define permissões dinâmicas com base na ação.
        """
        if self.action in ['create', 'login']:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Cria um novo usuário com senha criptografada.
        """
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"detail": "Cadastro realizado com sucesso"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        Autentica o usuário e gera tokens JWT.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Tenta autenticar o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({"message": "Login realizado com sucesso"}, status=status.HTTP_200_OK)

            # Adiciona o JWT como cookies HttpOnly
            response.set_cookie(
                key='jwt_access',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,  # Defina como True em produção
                samesite='Lax'
            )
            response.set_cookie(
                key='jwt_refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax'
            )

            # Log de sucesso na autenticação
            print(f"Usuário {username} autenticado com sucesso.")
            return response
        else:
            # Log de falha na autenticação
            print(f"Falha na autenticação para o usuário {username}.")
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Realiza logout removendo os cookies JWT.
        """
        response = Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt_access')
        response.delete_cookie('jwt_refresh')
        return response

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Retorna os detalhes do usuário autenticado.
        """
        user = request.user
        serializer = self.get_serializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
