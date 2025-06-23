from django.db import models
from django.utils import timezone
import string, random

class ShortURL(models.Model):
    original_url = models.URLField()
    shortcode = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_minutes = models.PositiveIntegerField(default=30)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=self.expiry_minutes)

    def __str__(self):
        return f"{self.shortcode} → {self.original_url}"

class ClickEvent(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name='clicks')
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Click on {self.short_url.shortcode} at {self.timestamp}"
