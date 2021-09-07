import itertools

from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from ordering.models import GenericMenuItem, Order
from ordering.serializers import MenuSerializer, OrderSerializer, OrderStatusSerializer, OrderCancelSerializer


class MenuListAPIView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        menu_items = list(self.get_queryset())
        result_dict = [(k, list(grp)) for k, grp in itertools.groupby(menu_items, key=lambda x: x.content_type)]
        serializer = MenuSerializer(result_dict, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return GenericMenuItem.objects.all()


class OrderCreateRetrieveAPIView(mixins.CreateModelMixin, mixins.ListModelMixin,
                                 GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrderStatusUpdateAPIView(generics.UpdateAPIView):
    serializer_class = OrderStatusSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser, ]

    def put(self, request, *args, **kwargs):
        pass


class OrderCancelUpdateAPIView(generics.UpdateAPIView):
    serializer_class = OrderCancelSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        pass