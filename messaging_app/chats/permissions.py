from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation, IsOwnerOrAdmin
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

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it
    and its messages.
    """
    def has_permission(self, request, view):
        # First check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Allow GET and POST requests for authenticated users
        if request.method in ['GET', 'POST']:
            return True
            
        # For PUT, PATCH, DELETE methods, check if user is participant in has_object_permission
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return True  # Actual permission check done in has_object_permission
            
        return False  # Deny other methods

    def has_object_permission(self, request, view, obj):
        # Allow admin users full access
        if request.user.is_staff:
            return True

        # If we're checking a Message object
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # If we're checking a Conversation object
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False
# ["conversation_id", "Message.objects.filter"]
"conversation_id", "Message.objects.filter"


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation, IsOwnerOrAdmin]
    
    def get_queryset(self):
        # Filter messages based on conversation_id if provided in query params
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.none()  # Return empty if no conversation_id provided
    
    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            if self.request.user in conversation.participants.all():
                serializer.save(user=self.request.user, conversation=conversation)
            else:
                raise PermissionDenied("You are not a participant of this conversation")
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found")