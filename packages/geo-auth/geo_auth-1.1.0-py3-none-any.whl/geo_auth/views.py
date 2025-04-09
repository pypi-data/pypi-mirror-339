from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .Serializer import UserSerializer


@api_view(["GET"])
def get_client_location_from_ip(request):
    ip_address = getattr(request, "ip_address", "Unknown")
    currency = request.currency
    location_data = request.location_data
    country_info = request.country_info
    device_info = request.device_info

    return Response({
        "client_ip": ip_address,
        "location_data": {
            "location": location_data,
            "country_info": country_info,
            "currency": currency
        },
        "device_info": device_info,
    })

@api_view(["GET"])
def get_client_ip(request):
    ip_address = request.ip_address
    return Response({
        "client_ip": ip_address,
    })

@api_view(["GET"])
def get_client_device_info(request):
    device_info = request.device_info
    return Response({
        "device_info": device_info,
    })

class UserRegistrationView(APIView):
    def post(self, request):
        # Pass the request object in the context to the serializer
        serializer = UserSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Save the user if validation passes
            serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": serializer.data,  # This includes the 'country' field
                "country": serializer.validated_data.get("country", "UNKNOWN")
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def health_check(request):
    return HttpResponse(status=200)
