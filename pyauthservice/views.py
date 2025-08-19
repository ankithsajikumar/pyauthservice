from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings

def home_redirect(request):
    return redirect(settings.HOME_URL)

@require_GET
def status_report(request):
    api_token = settings.SERVICE_API_TOKEN
    auth_header = request.headers.get(settings.SERVICE_API_TOKEN_KEY)
    if not api_token or auth_header != api_token:
        return JsonResponse({"detail": "Unauthorized"}, status=401)
    return JsonResponse({"status": "ok", "service": "pyauthservice"})