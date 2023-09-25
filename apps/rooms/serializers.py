from django.db.models import Q, Prefetch
from rest_framework import serializers
from .models import RoomType, Room, Reservation
import datetime



class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    room_type_info = RoomTypeSerializer(source='room_type', read_only=True)

    class Meta:
        model = Room
        fields = ('number', 'room_type', 'room_type_info')


class CreateReservationSerializer(serializers.ModelSerializer):
    '''
    This is for the guests or agents where they create a reservation by selecting
    the date range and a room type, then an available room is assigned if exists
    '''
    selected_room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all(), write_only=True)
    room_type = RoomTypeSerializer(source='assigned_room.room_type', read_only=True)

    class Meta: 
        model = Reservation
        fields = ('user', 'check_in_date', 'check_out_date', 'selected_room_type', 'room_type')

    def create(self, validated_data):
        selected_room_type = validated_data.pop('selected_room_type')
        check_in_date = validated_data['check_in_date']
        check_out_date = validated_data['check_out_date']

        # check if the date range is valid
        if check_in_date and check_out_date:
            if check_in_date > check_out_date:
                raise serializers.ValidationError("Check-in date cannot be later than check-out date")
        
        # check if the date range is not older than today
        today = datetime.datetime.now()
        if check_in_date < today.date():
            raise serializers.ValidationError("Check-in date should be in the future")

        # Find an available room of the selected room type within the date range
        available_room = None
        rooms = Room.objects.filter(room_type=selected_room_type).prefetch_related(
            Prefetch('reservations', queryset=Reservation.objects.filter(check_out_date__gte=today.date()))
        )
        for room in rooms:
            reservations = room.reservations.all()
            if not reservations.exists():
                available_room = room
                break
            has_conflicting_reservation = False
            for res in reservations:
                if res.check_in_date < check_out_date and res.check_out_date > check_in_date:
                    has_conflicting_reservation = True
                    break
            if not has_conflicting_reservation:
                available_room = room
                break
        
        if not available_room:
            raise serializers.ValidationError("No rooms available for the selected date range and room type.")
        
        validated_data['assigned_room'] = available_room
        
        return super().create(validated_data)
    

class GetReservationSerializer(serializers.ModelSerializer):

    assigned_room_info = RoomSerializer(source='assigned_room', read_only=True)

    class Meta:
        model = Reservation
        fields = ('user', 'check_in_date', 'check_out_date', 'assigned_room', 'assigned_room_info')


class UpdateDateRangeReservationSerializer(serializers.ModelSerializer):

    assigned_room_info = RoomSerializer(source='assigned_room', read_only=True)

    class Meta:
        model = Reservation
        fields = ('user', 'check_in_date', 'check_out_date', 'assigned_room', 'assigned_room_info')
        read_only_fields = ('user', 'assigned_room')

    def update(self, instance, validated_data):
        check_in_date = validated_data['check_in_date']
        check_out_date = validated_data['check_out_date']

        # check if the date range is valid
        if check_in_date and check_out_date:
            if check_in_date > check_out_date:
                raise serializers.ValidationError("Check-in date cannot be later than check-out date")
            
        # check if the assigned_room is available at the new date range
        room = instance.assigned_room
        conflicting_reservations = Reservation.objects.filter(
            assigned_room=instance.assigned_room,
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        ).exclude(pk=instance.pk)

        if conflicting_reservations.exists():
            raise serializers.ValidationError("There is a conflicting reservation with the same room and new date range.")
        
        return super().update(instance, validated_data)
    

class UpdateRoomReservationSerializer(serializers.ModelSerializer):

    assigned_room_info = RoomSerializer(source='assigned_room', read_only=True)

    class Meta:
        model = Reservation
        fields = ('user', 'check_in_date', 'check_out_date', 'assigned_room', 'assigned_room_info')
        read_only_fields = ('user', 'check_in_date', 'check_out_date')

    def update(self, instance, validated_data):
        new_assigned_room = validated_data['assigned_room']

        # check if the new assigned_room is available at the same date range
        conflicting_reservations = Reservation.filter(
            assigned_room=new_assigned_room,
            check_in_date__lt=instance.check_out_date,
            check_out_date__gt=instance.check_in_date
        ).objects.exclude(pk=instance.pk)

        if conflicting_reservations.exists():
            raise serializers.ValidationError("There is a conflicting reservation with the new room and the exisitng date range.")
        
        return super().update(instance, validated_data)