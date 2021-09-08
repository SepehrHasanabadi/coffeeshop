from django.urls import path

from ordering.views import MenuListAPIView, OrderCreateRetrieveAPIView, OrderStatusUpdateAPIView, OrderCancelUpdateAPIView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('menu/', MenuListAPIView.as_view()),
    path('order/', OrderCreateRetrieveAPIView.as_view()),
    path('order/<pk>/status/', OrderStatusUpdateAPIView.as_view()),
    path('order/<pk>/cancel/', OrderCancelUpdateAPIView.as_view()),
]