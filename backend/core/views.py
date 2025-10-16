from django.http import JsonResponse

def ping(request):
    """
    Simple healthcheck endpoint.
    Returns 200 OK when the backend is up.
    """
    return JsonResponse({"status": "ok"}, status=200)