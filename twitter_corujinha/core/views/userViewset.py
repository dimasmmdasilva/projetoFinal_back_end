from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import UserSerializer, RegisterUserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action in ['me', 'update_bio', 'update_profile_image']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_bio(self, request):
        user = request.user
        user.bio = request.data.get('bio', user.bio)
        user.save()
        return Response({'success': 'Biografia atualizada com sucesso'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile_image(self, request):
        user = request.user
        profile_image = request.FILES.get('profile_image')
        
        if profile_image:
            user.profile_image = profile_image
            user.save()
            
            # Retorna a URL completa da imagem
            profile_image_url = request.build_absolute_uri(user.profile_image.url)
            return Response({'profile_image_url': profile_image_url}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Imagem não fornecida'}, status=status.HTTP_400_BAD_REQUEST)