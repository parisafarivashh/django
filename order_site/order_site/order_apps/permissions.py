from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True


class IsOwn(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ActionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ('create', 'update', 'delete', 'partial_update'):
            return request.user.is_authenticated() and request.user.is_staff

