from django.middleware.csrf import get_token

class EnsureCsrfCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Forces Django to send CSRF cookie with every response
        get_token(request)
        response = self.get_response(request)
        return response