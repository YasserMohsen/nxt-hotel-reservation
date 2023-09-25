from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from .constants import ADMIN_USER, AGENT_USER, GUEST_USER


def _is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).users.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None

def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsOwnerOrHigherRole(BasePermission):
    required_groups = [ADMIN_USER, AGENT_USER]
    
    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return obj == request.user or has_group_permission
    

class IsOwnerOrOtherRoles(BasePermission):
    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return obj.user == request.user or has_group_permission
    
class IsOwnerOrAdminRole(IsOwnerOrOtherRoles):
    # group_name for admin users
    required_groups = [ADMIN_USER]


class IsOwnerOrAdminOrAgentRole(IsOwnerOrOtherRoles):
    # group_name for admin users
    required_groups = [ADMIN_USER, AGENT_USER]


class RoleBasePermission(BasePermission):
    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


class IsAdminRole(RoleBasePermission):
    required_groups = [ADMIN_USER]


class IsAgentRole(RoleBasePermission):
    required_groups = [AGENT_USER]


class IsGuestRole(RoleBasePermission):
    required_groups = [GUEST_USER]

        
