from django.contrib import admin
from .models import ShortURL, ClickEvent

admin.site.register(ShortURL)
admin.site.register(ClickEvent)
