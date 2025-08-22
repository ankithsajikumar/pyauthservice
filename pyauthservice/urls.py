from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from users import urls as users_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import home_redirect, status_report, login_page, login_view, logout_view

urlpatterns = [
    path('', home_redirect, name='home-redirect'),
    path('login/', login_page, name='login-page'),
    path('admin/', admin.site.urls),
    path('o/', include(oauth2_urls)),
    path('api/', include(users_urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', login_view, name='api_login'),
    path('api/logout/', logout_view, name='api_logout'),
    path('api/status/', status_report, name='status-report'),
]

admin.site.site_header = 'Auth Service Administration'
admin.site.index_title = 'User Management'
admin.site.site_title = 'Auth Service Admin'
