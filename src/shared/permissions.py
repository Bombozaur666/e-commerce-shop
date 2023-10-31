from rest_framework import permissions

from shared.utils import Roles


class IsClient(permissions.BasePermission):
    message = "You need to be a Client."

    def has_permission(self, request, view):
        if request.user.groups.filter(name=Roles.CLIENT).exists():
            return True


class IsSeller(permissions.BasePermission):
    message = "You need to be a Seller."

    def has_permission(self, request, view):
        if request.user.groups.filter(name=Roles.SELLER).exists():
            return True
