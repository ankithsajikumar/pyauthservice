from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from oauth2_provider import urls as oauth2_urls
from users import urls as users_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import login_view, logout_view, health

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False), name='home'),
    path('', include(oauth2_urls)),
    path('admin/', admin.site.urls),
    path('api/', include(users_urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', login_view, name='api_login'),
    path('api/logout/', logout_view, name='api_logout'),
    path('health/', health, name='health'),
    re_path(r'^.*$', RedirectView.as_view(url='/admin/', permanent=False)),
]

admin.site.site_header = 'Auth Service Administration'
admin.site.index_title = 'User Management'
admin.site.site_title = 'Auth Service Admin'
