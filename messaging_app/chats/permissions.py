from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation, IsOwnerOrAdmin

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