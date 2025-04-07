from django.urls import path

from .views import get_client_ip, get_client_location_from_ip, UserRegistrationView,get_client_device_info

urlpatterns = [
    path("ip/", get_client_ip, name="get_ip_auto"),
    path("location/", get_client_location_from_ip, name="process"),
    path("device/", get_client_device_info, name="device"),
    path("register/", UserRegistrationView.as_view(), name="register")
]
