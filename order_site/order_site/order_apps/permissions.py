from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True


class IsOwn(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


