from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import timedelta
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse

from .models import ShortURL, ClickEvent
from .serializers import ShortURLSerializer, ShortURLStatsSerializer


# Home endpoint (Optional, for root `/`)
def home(request):
    return JsonResponse({"message": "URL Shortener Microservice is running!"})


# Create Short URL: GET returns info, POST creates short URL
class CreateShortURLView(APIView):
    def get(self, request):
        return Response({"message": "Send a POST request to create a short URL."})

    def post(self, request):
        serializer = ShortURLSerializer(data=request.data)
        if serializer.is_valid():
            short_url_obj = serializer.save()
            expiry_time = short_url_obj.created_at + timedelta(minutes=short_url_obj.expiry_minutes)
            return Response({
                "shortLink": f"http://{request.get_host()}/{short_url_obj.shortcode}",
                "expiry": expiry_time.isoformat() + "Z"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Redirect Short URL: GET /<shortcode>
class RedirectShortURLView(APIView):
    def get(self, request, shortcode):
        url_obj = get_object_or_404(ShortURL, shortcode=shortcode)

        if url_obj.is_expired():
            return Response({"error": "This link has expired."}, status=410)

        # Log click event
        ClickEvent.objects.create(
            short_url=url_obj,
            referrer=request.META.get("HTTP_REFERER"),
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )
        return redirect(url_obj.original_url)


# Stats: GET /shorturls/<shortcode>
class ShortURLStatsView(APIView):
    def get(self, request, shortcode):
        url_obj = get_object_or_404(ShortURL, shortcode=shortcode)
        serializer = ShortURLStatsSerializer(url_obj)
        return Response(serializer.data)
