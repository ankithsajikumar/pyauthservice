from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def home_redirect(request):
    return redirect(settings.HOME_URL)

@require_GET
def status_report(request):
    api_token = settings.SERVICE_API_TOKEN
    auth_header = request.headers.get(settings.SERVICE_API_TOKEN_KEY)
    if not api_token or auth_header != api_token:
        return JsonResponse({"detail": "Unauthorized"}, status=401)
    return JsonResponse({"status": "ok", "service": "pyauthservice"}, status=200)

def login_page(request):
    css_url = getattr(settings, "LOGIN_PAGE_CSS", None)
    js_url = getattr(settings, "LOGIN_PAGE_JS", None)
    return render(request, "login.html", {"css_url": css_url, "js_url": js_url})