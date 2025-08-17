from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, MeView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('auth/me/', MeView.as_view(), name='me'),
]