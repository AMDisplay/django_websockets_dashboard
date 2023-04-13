from django.urls import path
from .consumers import DashboardConsumer


web_socket_urlpatterns = [
    path("ws/<str:dashboard_slug>/", DashboardConsumer.as_asgi()),
]