from rest_framework import serializers

from ordering.models import Order


class MenuItemSerializer(serializers.Serializer):

    def to_representation(self, instance):
        result = super(MenuItemSerializer, self).to_representation(instance)
        for field in instance.content_object._meta.fields:
            if field.name == 'id':
                result[field.name] = instance.id
                continue
            result[field.name] = getattr(instance.content_object, field.name)
        return result


class MenuSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj[0].model

    def get_options(self, obj):
        result = MenuItemSerializer(obj[1], many=True)
        return result.data


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    order = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'status', 'consume_location', 'menu_item', 'order', )

    def get_order(self, obj):
        serializer = MenuItemSerializer(obj.menu_item)
        data = serializer.data
        data['name'] = obj.menu_item.content_object._meta.verbose_name
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = super(OrderSerializer, self).create(validated_data)
        return instance


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)


class OrderCancelSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('status',)

    def update(self, instance, validated_data):
        validated_data['status'] = Order.CANCELED
        instance = super(OrderCancelSerializer, self).update(instance, validated_data)
        return instance
