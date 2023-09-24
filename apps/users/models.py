from django.db import models
from django.contrib.auth.models import AbstractUser, Group



class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True, blank=False)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='users')

    REQUIRED_FIELDS = ['email', 'role_id']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def __str__(self):
        if self.first_name or self.last_name:
            return ' '.join([self.first_name,self.last_name]).strip()
        else:
            return self.username
