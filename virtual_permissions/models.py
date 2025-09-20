from django.db import models

class ExternalPermissionAnchor(models.Model):
    """
    Dummy model to anchor all external/service permissions.
    """
    class Meta:
        verbose_name = "External Permission"
        verbose_name_plural = "External Permissions"
