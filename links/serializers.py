from rest_framework import serializers

from .models import Link, Category


class LinksSerializer(serializers.ModelSerializer):

    logo = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField(read_only=True)

    def get_logo(self, obj):
        if obj.logo:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.logo.image.url)
        return None

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return None

    class Meta:
        model = Link
        fields = (
            "id",
            "name",
            "description",
            "url",
            "created_by",
            "team",
            "logo",
            "category",
            "category_name",
        )


class CategorySerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField(read_only=True)

    def get_links(self, obj):
        request = self.context.get("request")
        links = Link.objects.filter(category=obj)
        return LinksSerializer(links, many=True, context={"request": request}).data

    class Meta:
        model = Category
        fields = (
            "id",
            "team",
            "name",
            "links",
        )

