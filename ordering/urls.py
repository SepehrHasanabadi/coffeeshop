from django.urls import path, include

# Routers provide an easy way of automatically determining the URL conf.
from rest_framework import routers

from ordering.views import MenuListAPIView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('menu/', MenuListAPIView.as_view()),
]