import django_filters
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    created_at = django_filters.DateFromToRangeFilter()  # ✅ Allows filtering by date range

    class Meta:
        model = Message
        fields = ['sender', 'created_at']