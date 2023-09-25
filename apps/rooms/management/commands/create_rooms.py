from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from apps.rooms.models import RoomType, Room


class Command(BaseCommand):
    def handle(self, *args, **options):
        '''
        Create some rome types and rooms
        '''
        data = [
            {
                'name': 'Sea View Room (small)',
                'description': 'Sea View Room with size 30 m2',
                'capacity': 2,
                'price_per_night': 120,
                'rooms': [
                    {'number': 'A101'},
                    {'number': 'A102'},
                ]
            },
            {
                'name': 'Sea View Room (large)',
                'description': 'Sea View Room with size 50 m2',
                'capacity': 4,
                'price_per_night': 200,
                'rooms': [
                    {'number': 'A103'},
                    {'number': 'A104'},
                ]
            },
            {
                'name': 'Pool View Room (small)',
                'description': 'Pool View Room with size 30 m2',
                'capacity': 2,
                'price_per_night': 100,
                'rooms': [
                    {'number': 'B101'},
                    {'number': 'B102'},
                ]
            },
            {
                'name': 'Pool View Room (large)',
                'description': 'Pool View Room with size 50 m2',
                'capacity': 4,
                'price_per_night': 180,
                'rooms': [
                    {'number': 'B103'},
                    {'number': 'B104'},
                ]
            }
        ]
        for d in data:
            rooms_data = d.pop('rooms')
            rt = RoomType.objects.create(**d)
            for r in rooms_data:
                Room.objects.create(room_type=rt, **r)
            self.stdout.write(self.style.SUCCESS((f'Room Type "{rt}" has been created successfully, and {len(rooms_data)} rooms have been added to it.')))