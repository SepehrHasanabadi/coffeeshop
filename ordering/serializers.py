from rest_framework import serializers

from ordering.models import MenuItem


class MenuItemSerializer(serializers.Serializer):

    def to_representation(self, instance):
        result = super(MenuItemSerializer, self).to_representation(instance)
        for field in instance.content_object._meta.fields:
            if field.name == 'id':
                continue
            result[field.name] = getattr(instance.content_object, field.name)
        return result


class MenuSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    attrs = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj[0].model

    def get_attrs(self, obj):
        result = MenuItemSerializer(obj[1], many=True)
        return result.data
