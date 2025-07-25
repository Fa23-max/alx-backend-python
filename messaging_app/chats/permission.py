from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a message/conversation to access it.
    Admins have full access.
    """
    def has_object_permission(self, request, view, obj):
        # Admin permissions
        if request.user.is_staff:
            return True
            
        # Check if the object has a user field directly
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        # Check if the object has a participants field (for conversations)
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
            
        return False

    def has_permission(self, request, view):
        # Deny permission for unauthenticated users
        return request.user and request.user.is_authenticated
