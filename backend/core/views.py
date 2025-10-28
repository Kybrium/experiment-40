from django.http import JsonResponse
from django.utils import translation


def ping(request):
    """
    Lightweight healthcheck + i18n debug endpoint.

    - "status": "ok" means the server is reachable and responding.
    - "lang": request.LANGUAGE_CODE as set by UserLanguageMiddleware.
    - "active_lang": current thread's active language from django.utils.translation.
    """
    return JsonResponse(
        {
            "status": "ok",
            "lang": getattr(request, "LANGUAGE_CODE", None),
            "active_lang": translation.get_language(),
        },
        status=200,
    )