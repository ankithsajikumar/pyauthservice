from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

#To-do: add proper health check and request scope.
def health(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(
            request,
            username=data.get("username"),
            password=data.get("password")
        )
        if user:
            login(request, user)
            return JsonResponse({"status": "ok"})
        return JsonResponse({"error": "Invalid credentials"}, status=400)
    
@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"status": "ok", "message": "logged out"})
    return JsonResponse({"error": "Invalid method"}, status=405)
