from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_staff:
            return False


class IsOwn(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return obj.user == request.user


