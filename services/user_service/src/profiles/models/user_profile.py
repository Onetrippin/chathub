import uuid

from django.db import models


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth_id = models.UUIDField()  # связь с AuthUser из Auth Service
    timezone = models.CharField(max_length=64, default='UTC')
    language = models.CharField(max_length=16, default='ru')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profile'
