import itertools

from rest_framework import generics
from rest_framework.response import Response

from ordering.models import GenericMenuItem
from ordering.serializers import MenuSerializer


class MenuListAPIView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        menu_items = list(self.get_queryset())
        result_dict = [(k, list(grp)) for k, grp in itertools.groupby(menu_items, key=lambda x: x.content_type)]
        serializer = MenuSerializer(result_dict, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return GenericMenuItem.objects.all()
