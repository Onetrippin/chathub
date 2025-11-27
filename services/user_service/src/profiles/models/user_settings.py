import uuid

from django.db import models


class UserSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    ai_persona = models.CharField(max_length=64, default='default')
    notifications_enabled = models.BooleanField(default=True)
    theme = models.CharField(max_length=16, default='light')

    class Meta:
        db_table = 'user_settings'