from django.contrib import admin
from django.contrib.auth.models import Permission

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "codename", "content_type")
    search_fields = ("name", "codename", "content_type__app_label")
    list_filter = ("content_type__app_label",)
