from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .utility import get_location_from_ip


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    country = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password", "country"]
        extra_kwargs = {"password": {"write_only": True}}
    
    
    
    def validate_email(self, value):
        """handle email validation """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def validate(self, data):
        """ handle country and password validation """
        request = self.context.get("request")
        if not request:
            raise ValidationError({"error": ["Request object is missing."]})

        # get ip address from request
        ip_address = getattr(request, "ip_address", None)
        location_data = get_location_from_ip(ip_address)

        allowed_countries = settings.ALLOWED_COUNTRIES

        country_name = location_data.get("country", "")
        country_code = location_data.get("country_code")

        allowed_countries_lower = [c.lower() for c in allowed_countries]

        data["country"] = {
            "name":country_name.title(),
            "code": country_code.upper()
            }

    # Ensure the country is allowed
        if country_code not in allowed_countries and country_name not in allowed_countries_lower:
            raise serializers.ValidationError({
                "error": "Registration from this country is not allowed.",
                "country": data["country"] 
                })
        
        if len(data['password']) < 8:
            raise ValidationError("Password must be at least eight characters long.")

        if data['confirm_password'] != data['password']:
            raise ValidationError("Confirm password and password must match.")

        return data

    def create(self, validated_data):
        """
        create the user without saving the confirm_passowrd and the country if not in the model instance
        
        """
        validated_data.pop("confirm_password", None)
        validated_data.pop("country", None)
        user = User.objects.create_user(**validated_data)
        return user