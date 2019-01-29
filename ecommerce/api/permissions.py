from rest_framework import permissions
from api.models import APIClient


class IsNotHacker(permissions.BasePermission):

    # view level permission
    def has_permission(self, request, view):
        if isinstance(request.user, APIClient):
            name = request.user.name
        else:
            name = request.user.username

        if 'hacker' in name.lower():
            return False
        return True


class IsOddProductID(permissions.BasePermission):

    # object level permission
    def has_object_permission(self, request, view, obj):
        product = obj
        if product.id % 2 == 1:
            return True
        return False
