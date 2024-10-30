from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TweetViewSet, CommentViewSet, FollowViewSet

# Cria o roteador e registra as rotas para as views
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tweets', TweetViewSet, basename='tweet')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'follows', FollowViewSet, basename='follow')

# Incluindo as URLs do router no padrão urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
