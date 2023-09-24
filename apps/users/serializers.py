from django.contrib.auth import get_user_model, models
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .constants import GUEST_USER


User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('name',)
        model = models.Group


class UserSerializer(serializers.ModelSerializer):
    '''
    Generic user serializer to apply all actions
    '''

    role_name = serializers.CharField(source='role.name', required=False)
    
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'role', 'role_name', 'email')
        read_only_fields = ('role_name',)
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        # handle password validation as it is not handled in DRF by default
        try:
            validate_password(password=validated_data['password'], user=user)
        except ValidationError as err:
            user.delete()
            raise serializers.ValidationError({'password': err.messages})
        return user
    

class RegistrationSerializer(serializers.ModelSerializer):
    '''
    To be used by guests only for registration. The main difference between this serializer 
    and the pervious one is that role field value is being set implicitly as GUEST_USER
    and not exposed to the user to define his role.
    '''

    role_name = serializers.CharField(source='role.name', required=False)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'role', 'role_name', 'email')
        read_only_fields = ('role', 'role_name')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = models.Group.objects.get(name=GUEST_USER)
        user = User.objects.create(role=role, **validated_data)
        user.set_password(validated_data['password'])
        user.save()
        # handle password validation as it is not handled in DRF by default
        try:
            validate_password(password=validated_data['password'], user=user)
        except ValidationError as err:
            user.delete()
            raise serializers.ValidationError({'password': err.messages})
        return user