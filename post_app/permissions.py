from rest_framework import permissions


class IsOwnerOrReadOnlyPost(permissions.BasePermission):
    """
    Object-level permission to only allow users to edit/update/remove theirs
    posts.
    Assumes the model instance has an `author` attribute and the latter has id.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author.id == request.user.id
