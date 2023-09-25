from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, 
    RetrieveModelMixin, 
    ListModelMixin, 
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdminRole, IsAgentRole, IsOwnerOrAdminOrAgentRole
from .models import RoomType, Room, Reservation
from .serializers import (
    RoomTypeSerializer,
    RoomSerializer,
    CreateReservationSerializer,
    GetReservationSerializer,
    UpdateDateRangeReservationSerializer,
    UpdateRoomReservationSerializer
)


class RoomTypeViewSet(ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminRole]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminRole]
        elif self.action == 'destroy':
            permission_classes = [IsAdminRole]
        return [permission() for permission in permission_classes]
    

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminRole]
        elif self.action == 'list':
            permission_classes = [IsAdminRole|IsAgentRole]
        elif self.action == 'retrieve':
            permission_classes = [IsAdminRole|IsAgentRole]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminRole]
        elif self.action == 'destroy':
            permission_classes = [IsAdminRole]
        return [permission() for permission in permission_classes]
    

class CreateReservationViewSet(CreateModelMixin, GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = CreateReservationSerializer
    permission_classes = [IsAuthenticated]  # TODO: need to prevent the guest user from a reservation for another user


class GetReservationViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = GetReservationSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAdminRole|IsAgentRole]  # TODO: Guest user should be able to list his reservations only
        elif self.action == 'retrieve':
            permission_classes = [IsOwnerOrAdminOrAgentRole]
        elif self.action == 'destroy':
            permission_classes = [IsAdminRole|IsAgentRole]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(check_out_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(check_in_date__gte=end_date)
        return queryset
    

class UpdateDateRangeReservationViewSet(UpdateModelMixin, GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = UpdateDateRangeReservationSerializer
    permission_classes = [IsAdminRole|IsAgentRole]


class UpdateRoomReservationViewSet(UpdateModelMixin, GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = UpdateRoomReservationSerializer
    permission_classes = [IsAdminRole|IsAgentRole]