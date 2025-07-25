import datetime
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.http import HttpResponseForbidden
class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request with user, timestamp, and path
        log_entry = f"{datetime.datetime.now()} - User: {request.user} - Path: {request.path}\n"
        with open(settings.BASE_DIR / 'request_log.txt', 'a') as f:
            f.write(log_entry)
        
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.now().time()
        # Allow access between 6 PM (18:00) and 9 PM (21:00)
        if not (datetime.time(18, 0) <= now < datetime.time(21, 0)):
            return HttpResponseForbidden("Access denied outside allowed hours (6 PM - 9 PM).")
        
        response = self.get_response(request)
        return response
    

import time
from collections import defaultdict
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    message_counts = defaultdict(list)  # Tracks IP message timestamps

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to POST requests to chat messages (adjust path as needed)
        if request.method == 'POST' and request.path.startswith('/chats/messages/'):
            ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Remove timestamps older than 1 minute (60 seconds)
            self.message_counts[ip] = [t for t in self.message_counts[ip] if current_time - t < 60]
            
            # Check if message limit is exceeded
            if len(self.message_counts[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded (5 messages per minute).")
                
            # Add current timestamp to the list
            self.message_counts[ip].append(current_time)
        
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
    



class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and has admin/moderator role
        if request.user.is_authenticated:
            if not (request.user.is_admin or request.user.is_moderator):
                return HttpResponseForbidden("Access denied. Admin or Moderator role required.")
        else:
            return HttpResponseForbidden("Access denied. Authentication required.")
        
        response = self.get_response(request)
        return response