from rest_framework import serializers
from .models import ShortURL, ClickEvent
from .utils import generate_shortcode


# Serializer for creating a short URL
class ShortURLSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    validity = serializers.IntegerField(required=False, default=30)
    shortcode = serializers.CharField(required=False)

    def validate_shortcode(self, value):
        if ShortURL.objects.filter(shortcode=value).exists():
            raise serializers.ValidationError("Shortcode already exists.")
        return value

    def create(self, validated_data):
        original_url = validated_data['url']
        validity = validated_data.get('validity', 30)
        shortcode = validated_data.get('shortcode')

        if not shortcode:
            shortcode = generate_shortcode()

        return ShortURL.objects.create(
            original_url=original_url,
            shortcode=shortcode,
            expiry_minutes=validity
        )


# Serializer for individual click events (for stats)
class ClickEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickEvent
        fields = ['timestamp', 'referrer', 'ip_address', 'user_agent']


# Serializer for stats response
class ShortURLStatsSerializer(serializers.ModelSerializer):
    clicks = ClickEventSerializer(many=True, read_only=True)
    total_clicks = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ['original_url', 'shortcode', 'created_at', 'expiry_minutes', 'clicks', 'total_clicks']

    def get_total_clicks(self, obj):
        return obj.clicks.count()
