from rest_framework import serializers

from ordering.models import Order

from ordering.tasks import send_modified_status_mail, send_cancel_order_mail


class MenuItemSerializer(serializers.Serializer):
    """
    every item is derived from MenuItem children like Latte,...
    this a generic serializer that makes a proper output base on the Menu item children
    """
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
        """
        :param obj: this is a (GenericMenuItem, groub) tuple. the first item can be cast to
        a MenuItem Child
        :return: content object model name
        """
        return obj[0].model

    def get_options(self, obj):
        """
        obj: this is a (GenericMenuItem, groub) tuple. the second item is an iteratable
        list which is the list of options for a menu child
        :param obj:
        :return: list of options
        """
        result = MenuItemSerializer(obj[1], many=True)
        return result.data


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    order = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'status', 'consume_location', 'menu_item', 'order', )

    def get_order(self, obj):
        """
        order is the menu item which is sent in the order request
        :param obj: order instance
        :return: menu item child
        """
        serializer = MenuItemSerializer(obj.menu_item)
        data = serializer.data
        data['name'] = obj.menu_item.content_object._meta.verbose_name
        return data

    def create(self, validated_data):
        """
        authenticated user would be set as the owner of an order
        :param validated_data: consume_location and menu_item
        :return: order instance
        """
        validated_data['user'] = self.context['request'].user
        instance = super(OrderSerializer, self).create(validated_data)
        return instance


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)

    def create(self, validated_data):
        """
        send a proper mail to user of the order
        :param validated_data: status should be declared
        :return: order instance
        """
        instance = super(OrderStatusSerializer, self).create(validated_data)
        send_modified_status_mail([instance.user.email])
        return instance


class OrderCancelSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('status',)

    def update(self, instance, validated_data):
        """
        set cancel status to the order sent to be canceled
        send a proper mail to user of the order
        :param instance: order
        :param validated_data: should be empty
        :return: order instance
        """
        validated_data['status'] = Order.CANCELED
        instance = super(OrderCancelSerializer, self).update(instance, validated_data)
        send_cancel_order_mail([instance.user.email])
        return instance
