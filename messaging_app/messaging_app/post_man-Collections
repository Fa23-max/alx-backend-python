from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

class MessagingAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.conversation_data = {
            'title': 'Test Conversation',
            'participants': [self.user1.id, self.user2.id]
        }
        self.message_data = {
            'content': 'Hello, user2!',
            'conversation_id': 1
        }

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_jwt_authentication(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'user1', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_create_conversation(self):
        url = reverse('conversation-list')
        token = self.get_jwt_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(url, {'title': 'Private Chat'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        conversation = Conversation.objects.get(id=response.data['id'])
        self.assertIn(self.user1, conversation.participants.all())

    def test_send_message(self):
        # Create conversation first
        conversation = Conversation.objects.create(title='Test Chat')
        conversation.participants.add(self.user1)
        url = reverse('message-list')
        token = self.get_jwt_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(url, {
            'content': 'Test message',
            'conversation_id': conversation.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = Message.objects.get(id=response.data['id'])
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.conversation, conversation)

    def test_fetch_conversations(self):
        url = reverse('conversation-list')
        token = self.get_jwt_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Assuming one conversation exists

    def test_unauthorized_conversation_access(self):
        # User1 creates a conversation
        conversation = Conversation.objects.create(title='Private Chat')
        conversation.participants.add(self.user1)

        # User2 tries to fetch it (not a participant)
        url = reverse('conversation-detail', args=[conversation.id])
        token = self.get_jwt_token(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_message_access(self):
        # User1 creates a conversation and sends a message
        conversation = Conversation.objects.create(title='Private Chat')
        conversation.participants.add(self.user1)
        Message.objects.create(content='Secret message', sender=self.user1, conversation=conversation)

        # User2 tries to fetch messages in the conversation
        url = reverse('message-list') + f'?conversation_id={conversation.id}'
        token = self.get_jwt_token(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_message_pagination(self):
        # Create conversation and add 25 messages
        conversation = Conversation.objects.create(title='Paginated Chat')
        conversation.participants.add(self.user1)
        for i in range(25):
            Message.objects.create(content=f'Message {i}', sender=self.user1, conversation=conversation)

        # Fetch messages with pagination
        url = reverse('message-list') + f'?conversation_id={conversation.id}'
        token = self.get_jwt_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)  # Page 1
        self.assertEqual(response.data['count'], 25)  # Total messages

        # Fetch page 2
        response = self.client.get(url + '&page=2')
        self.assertEqual(len(response.data['results']), 5)  # Page 2
