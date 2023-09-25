from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdminRole, IsAgentRole, IsOwnerOrHigherRole
from .serializers import UserSerializer, RegistrationSerializer


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminRole]
        elif self.action == 'list':
            permission_classes = [IsAdminRole|IsAgentRole]
        elif self.action == 'retrieve':
            permission_classes = [IsOwnerOrHigherRole]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminRole]
        elif self.action == 'destroy':
            permission_classes = [IsAdminRole]
        return [permission() for permission in permission_classes]
    

class RegistrationViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
