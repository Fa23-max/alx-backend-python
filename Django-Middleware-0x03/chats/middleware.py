import datetime
from django.conf import settings

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
