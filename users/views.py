from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

class AllowPostAnyAuthenticatedOtherwise(permissions.BasePermission):
    """
    Allow anyone to POST (create user), require authentication for other methods.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowPostAnyAuthenticatedOtherwise]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
