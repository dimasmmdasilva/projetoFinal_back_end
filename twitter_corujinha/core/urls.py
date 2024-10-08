from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TweetViewSet, CommentViewSet, LikeViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tweets', TweetViewSet, basename='tweet')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'follows', FollowViewSet, basename='follow')

# Incluindo as URLs do router no padrão urlpatterns
urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', UserViewSet.as_view({'get': 'me'})),
]