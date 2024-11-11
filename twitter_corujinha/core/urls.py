from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TweetViewSet, CommentViewSet, FollowViewSet, UpdateProfileImageView
from .views import LoginView, LogoutView

# Criação do roteador e registro das rotas principais para as views do projeto
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tweets', TweetViewSet, basename='tweet')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'follows', FollowViewSet, basename='follow')

# Definição das URLs do módulo core
urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),  # Endpoint para login do usuário
    path('auth/logout/', LogoutView.as_view(), name='logout'),  # Endpoint para logout do usuário
    path('auth/token/refresh/', LoginView.as_view(), name='token_refresh'),  # Endpoint para refresh do token
    path('users/update_profile_image/', UpdateProfileImageView.as_view(), name='update_profile_image'),  # Endpoint para atualizar imagem de perfil
]
