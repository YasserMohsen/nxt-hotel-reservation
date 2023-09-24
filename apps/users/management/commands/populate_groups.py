from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from apps.users.constants import ADMIN_USER, AGENT_USER, GUEST_USER


class Command(BaseCommand):
    def handle(self, *args, **options):
        '''
        Create needed groups if not exist or update. Added with 'id' mentioned
        explicitly so that we can change the group name easily later,
        as the existance of a group here is defined by its 'id'
        '''
        for id, name in [
            (1, ADMIN_USER), 
            (2, AGENT_USER), 
            (3, GUEST_USER)
        ]:
            try:
                g = Group.objects.get(pk=id)
                if g.name != name:
                    old_name = g.name
                    g.name = name
                    g.save()
                    self.stdout.write(self.style.SUCCESS((f'Group "{old_name}" has been renamed to "{name}".')))
                else:
                    self.stdout.write(self.style.SUCCESS((f'Group "{name}" does exist already.')))
            except ObjectDoesNotExist:
                g = Group.objects.create(pk=id, name=name)
                self.stdout.write(self.style.SUCCESS((f'Group "{name}" has been created successfully.')))


            