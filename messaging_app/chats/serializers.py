from rest_framework import serializers
# Import your models from the same app.
# If you're using Django's built-in User model, uncomment the line below
# and comment out 'from .models import User'
# from django.contrib.auth import get_user_model
# User = get_user_model()
from .models import User, Conversation, Message

# Explicitly added imports as requested:
from rest_framework.exceptions import ValidationError # Correct import path for ValidationError


# --- 1. User Serializer ---
# This serializer is for full user details when you're directly interacting with User objects.
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, providing full details.
    """
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at'] # These fields are set automatically


# --- 2. SimpleUserSerializer (for nesting) ---
# This simplified serializer is used when you want to embed user information
# within other serializers (like Message or Conversation) without pulling
# all user details or creating circular dependencies.
class SimpleUserSerializer(serializers.ModelSerializer):
    """
    A simplified serializer for User, used when nesting User objects
    to prevent excessive data or circular dependencies.
    """
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email']
        read_only_fields = ['user_id', 'first_name', 'last_name', 'email'] # All fields read-only when nested


# --- 3. Message Serializer ---
# This serializer handles individual messages.
# It nests sender and recipient details using SimpleUserSerializer.
class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes nested representation of sender and recipient, and handles
    linking to a conversation.
    """
    # Read-only nested representation for sender and recipient.
    # This will display the details of the User object instead of just their ID.
    sender = SimpleUserSerializer(read_only=True)
    recipient = SimpleUserSerializer(read_only=True)

    # Write-only fields for creating/updating relationships by ID.
    # These are used when sending POST/PUT requests.
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='sender', write_only=True, required=True
    )
    recipient_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='recipient', write_only=True, required=True
    )
    # The conversation ID is required when creating a message to link it.
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(), source='conversation', write_only=True, required=True
    )

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation', # Displays the conversation's PK (UUID) when reading
            'sender',       # Nested sender object (read-only)
            'recipient',    # Nested recipient object (read-only)
            'message_body',
            'sent_at',
            # Fields used for writing (creating/updating relationships by ID)
            'sender_id',
            'recipient_id',
            'conversation_id'
        ]
        read_only_fields = ['message_id', 'conversation', 'sent_at'] # 'conversation' is read-only here for display, but settable via 'conversation_id'


# --- 4. Conversation Serializer ---
# This serializer handles conversations and includes all associated messages.
class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Handles nested messages and participants.
    """
    # Nested representation for messages within this conversation.
    # `many=True` because a conversation can have many messages.
    # `read_only=True` because messages are typically created via their own endpoint,
    # or a dedicated nested endpoint, not directly when creating/updating a conversation.
    # `source='messages'` refers to the `related_name` on the Message model's ForeignKey to Conversation.
    messages = MessageSerializer(many=True, read_only=True)

    # Nested representation for participants (Many-to-Many field).
    # This will show the simplified user details for each participant.
    participants = SimpleUserSerializer(many=True, read_only=True)

    # Write-only field for setting participants by their IDs when creating/updating a conversation.
    # `many=True` because it's a Many-to-Many relationship.
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source='participants', required=False
    )

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',     # Read-only nested participants
            'messages',         # Read-only nested messages (this is the "nested messages within a conversation")
            'created_at',
            'updated_at',
            'participant_ids'   # Write-only field for setting participants by ID
        ]
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    # Custom create method to handle the many-to-many 'participants' field
    # as it's not directly handled by ModelSerializer's default create/update for M2M.
    def create(self, validated_data):
        participants_data = validated_data.pop('participants', []) # Pop participants data
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants_data) # Set participants after conversation is created
        return conversation

    # Custom update method to handle the many-to-many 'participants' field
    def update(self, instance, validated_data):
        participants_data = validated_data.pop('participants', None) # Pop participants data
        instance = super().update(instance, validated_data) # Perform default update
        if participants_data is not None:
            instance.participants.set(participants_data) # Update participants if provided
        return instance

