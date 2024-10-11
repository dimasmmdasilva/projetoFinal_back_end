from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TweetViewSet, CommentViewSet, LikeViewSet, FollowViewSet

# Cria um router padrão do DRF
router = DefaultRouter()

# Registra os viewsets no router
router.register(r'users', UserViewSet, basename='user')
router.register(r'tweets', TweetViewSet, basename='tweet')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'follows', FollowViewSet, basename='follow')

# Inclui as URLs geradas pelo router no urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Inclui todas as rotas registradas no router
]
