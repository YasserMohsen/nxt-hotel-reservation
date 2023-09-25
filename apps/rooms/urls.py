from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomTypeViewSet,
    RoomViewSet,
    CreateReservationViewSet,
    GetReservationViewSet,
    UpdateDateRangeReservationViewSet,
    UpdateRoomReservationViewSet
)


router = DefaultRouter()
router.register('roomtypes', RoomTypeViewSet, basename='room-types')
router.register('rooms', RoomViewSet, basename='rooms')
router.register('reservation', CreateReservationViewSet, basename='new-reservation')
router.register('reservations', GetReservationViewSet, basename='reservations')
router.register('updatereservationdates', UpdateDateRangeReservationViewSet, basename='reservation-dates')
router.register('updatereservationroom', UpdateRoomReservationViewSet, basename='reservation-room')

urlpatterns = [
    path('', include(router.urls))
]