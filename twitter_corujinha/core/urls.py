from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TweetViewSet, CommentViewSet, LikeViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'follows', FollowViewSet)

# Incluindo as URLs do router no padrão urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
