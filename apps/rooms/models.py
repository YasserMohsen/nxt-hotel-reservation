from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    price_per_night = models.PositiveIntegerField()

    class Meta:
        ordering = ('capacity',)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=10)    # added as CharField because nuber could be something like: A104

    class Meta:
        ordering = ('room_type',)

    def __str__(self) -> str:
        return f"{self.room_type}: {self.number}"
    

class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='reservations')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    assigned_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')

    @property
    def nights_count(self):
        return (self.check_out_date - self.check_in_date).days
    
    @property
    def cost(self):
        if not self.assigned_room:
            return 0
        return self.assigned_room.room_type.price_per_night * self.nights_count

    class Meta:
        ordering = ('-check_in_date',)
        
    def __str__(self) -> str:
        return f"{self.user}'s reservation of room {self.assigned_room} from {self.check_in_date} to {self.check_out_date}"