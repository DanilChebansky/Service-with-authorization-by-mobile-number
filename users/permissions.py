from rest_framework.permissions import BasePermission


class IsSelfUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
