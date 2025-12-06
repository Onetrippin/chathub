import uuid
from django.db import models


class AuthUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    photo_url = models.URLField(null=True, blank=True)

    auth_date = models.DateTimeField(null=True, blank=True)  # из Telegram initData
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.telegram_id} ({self.username or '-'})"


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="refresh_tokens")
    token = models.CharField(max_length=512, unique=True, db_index=True)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"refresh({self.user_id})"