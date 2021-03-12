from rest_framework import permissions

class UserAuthorPermission(permissions.BasePermission):
    """
    User cant follow himself
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user