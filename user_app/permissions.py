from rest_framework import permissions


class IsOwnerOrReadOnlyUserProfile(permissions.BasePermission):
    """
    Object-level permission to only allow users to edit theirs profile.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
