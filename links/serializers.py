from rest_framework import serializers

from .models import Link

class LinksSerializer(serializers.ModelSerializer):

    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        if obj.logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.logo.image.url)
        return None
        
    class Meta:
        model = Link
        fields = (
            "name",
            "description",
            "url",
            "created_by",
            "team",
            "logo",
        )
