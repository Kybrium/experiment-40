from django.conf import settings
from django.http import HttpResponse
from django.utils import translation

class MaintenanceModeMiddleware:
    """
    Middleware that checks if the site is in maintenance mode.
    If the MAINTENANCE_MODE setting is True, it return a "Site under maintenance" response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE_MODE', False):
            return HttpResponse("Site is under maintenance", status=503)
        return self.get_response(request)
    

class UserLanguageMiddleware:
    """
    Middleware that synchronizes language with backend
    and frontend.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = None

        if request.user.is_authenticated:
            lang = getattr(request.user, "preferred_language", None)

        header_lang = request.headers.get("Accept-Language")
        active_lang = header_lang or lang or "en"

        translation.activate(active_lang)
        request.LANGUAGE_CODE = active_lang

        response = self.get_response(request)
        translation.deactivate()
        return response