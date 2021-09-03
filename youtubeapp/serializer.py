from rest_framework import serializers
from .models import Visitor


class Visitorserializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'ip',
            'country_code',
            'country_name',
            'time_zone',
            'latitude',
            'longitude',
            'ytd_request_link',
            'video_title',
            'video_thumb_img',
            'date_created',
            'time_created',
        )
        
        model = Visitor