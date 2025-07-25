from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.response import Response
from .permissions import IsParticipantOfConversation, IsOwnerOrAdmin

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        """
        Filter conversations to return only those where the user is a participant
        """
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """
        Add the creator as a participant when creating a new conversation
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages within conversations.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Filter messages to return only those from conversations where the user is a participant
        """
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        Set the sender to the current user when creating a message
        """
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)


# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .models import Conversation, Message
# from .serializers import MessageSerializer
# from .permissions import IsParticipantOfConversation, IsOwnerOrAdmin

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


# ["conversation_id", "Message.objects.filter"]