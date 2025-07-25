from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation, IsOwnerOrAdmin
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend  # ✅ Import for filtering
from .filters import MessageFilter  # ✅ Import the new filter class


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
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]  # ✅ Enable filtering
    filterset_class = MessageFilter  # ✅ Use the custom filter class

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
                serializer.save(sender=self.request.user, conversation=conversation)
            else:
                raise PermissionDenied("You are not a participant of this conversation")
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found")