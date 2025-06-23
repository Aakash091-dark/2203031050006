from django.urls import path
from .views import CreateShortURLView, RedirectShortURLView, ShortURLStatsView, home

urlpatterns = [
    path('', home),  # 👈 Home route added
    path('shorturls', CreateShortURLView.as_view(), name='create_short_url'),
    path('shorturls/<str:shortcode>', ShortURLStatsView.as_view(), name='short_url_stats'),
    path('<str:shortcode>', RedirectShortURLView.as_view(), name='redirect_short_url'),
]
