# GeoAuth Plugin Documentation

## 📌 Overview
GeoAuth is a Django plugin that provides authentication and user-related utilities with geo-location support. It allows users to:

### 1️⃣ Retrieve their website visitors' IP address.
### 2️⃣ Fetch device information (browser, OS, etc.).
### 3️⃣ Obtain location data (country, city, region, latitude, longitude).
### 4️⃣ Get country details (languages, timezone, currency, etc.).
### 5️⃣ Restrict user registration based on allowed countries.

## 🚀 Installation

### Using pip
```sh
pip install geo-auth
```

### Using Source Code
```sh
git clone https://github.com/shoileazeez/drf_geodata.git  
cd geo_auth 
pip install -r requirements.txt  
```

---

## ⚙️ Setup & Configuration

### 1️⃣ Add to Installed Apps
Modify `settings.py`:
```python
INSTALLED_APPS = [
    # Other apps...
    'geo_auth',
]
```

### 2️⃣ Run Migrations
```sh
python manage.py migrate
```

### 3️⃣ Configure Middleware (Optional)
If you want automatic geo-data retrieval, add the middleware in `settings.py`:
```python
MIDDLEWARE = [
    # Other middleware...
    'geo_auth.middleware.GeoAuthMiddleware',
]
```

### 4️⃣ Enable Plugin URLs
Users should add your plugin’s URLs in their `urls.py`:
```python
from django.urls import path, include  

urlpatterns = [
    # Other URLs...
    path('geo_auth/', include('geo_auth.urls')),  # Enable Goe Auth Plugin API
]
```

---

## 🔑 Token Configuration

1. Retrieve the database token from **[IP2Location Lite](https://lite.ip2location.com/)** after registration.
2. Add the token to the environment variables:

   ```sh
   export TOKEN="your_api_token_here"
   ```

3. Modify `settings.py` to retrieve the token dynamically:
   ```python
   import os

   TOKEN = os.getenv("TOKEN")
   ```
## 🌍 GeoNames Username Configuration

1. Register for a free account at **[GeoNames](https://www.geonames.org/login)**.
2. Use the same username you registered with and configure it as an environment variable:
3. Modify `settings.py` to retrieve the username dynamically:
   ```python
   import os

   GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")
   ```

# 🔌 How to Use the Geo Plugin

## 🚀 Middleware Usage Options

### Option 1: Automatic Retrieval
Middleware automatically attaches geo-data to each request.

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

def example_view(request):
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
```

✅ **Best for**: Users who want automatic access to all geo-data in their views.

### Option 2: API Views with Middleware
Using the middleware with dedicated API views for specific geo-data:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def get_client_ip_auto(request):
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
def get_client_location_from_ip(request):
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
```

✅ **Best for**: Users who want dedicated endpoints for retrieving specific geo-data while still using the middleware.

## 🛠️ Utility Functions Usage

### Option 3: Direct Function Calls
If you prefer calling functions manually, you can import and use utility functions:

```python
from geo_auth.utils import get_client_ip, get_device_info, get_location_data
from django.http import JsonResponse

def example_view(request):
    data = {
        "ip": get_client_ip(request),
        "device": get_device_info(request),
        "location": get_location_data(request),
    }
    return JsonResponse(data)
```

✅ **Best for**: Users who only need geo-data in specific views and prefer not to use middleware.

## 🔗 API Endpoints Usage

### Option 4: Using Pre-configured API Endpoints
Access geo-data directly through provided URLs after including the plugin's URLs in your project.

```python
# In your main urls.py
from django.urls import path, include

urlpatterns = [
    # Other URLs...
    path('geo_auth/', include('geo_auth.urls')),
]
```

Available endpoints:

```
GET /geo_auth/ip/
# Returns the client's IP address
# Example response: {"client_ip": "198.51.100.42"}

GET /geo_auth/device/
# Returns detailed information about the client's device
# Example response: {"device_info": {"browser": "Chrome", "os": "Windows", "device": "Desktop"}}

GET /geo_auth/location/
# Returns comprehensive location data based on the client's IP
# Example response: {"location_data": {"city": "New York", "country": "United States", "latitude": 40.7128, "longitude": -74.0060}}
```

✅ **Best for**: Projects that need quick access to geo-data without writing custom views.

### Option 5: Using Hosted API Service
For users who prefer not to install the plugin, you can use our hosted API service to get the same geo-data with simple HTTP requests:

```
GET https://api.geoauth.example.com/ip/
GET https://api.geoauth.example.com/device/
GET https://api.geoauth.example.com/location/
```

Example code to access the hosted API:

**1. Python - Requests Library**
```python
import requests

# Get location data
response = requests.get('https://api.geoauth.example.com/location/')
data = response.json()
print(data)
```

**2. Python - Standard Library (urllib)**
```python
import json
import urllib.request

# Get device info
with urllib.request.urlopen('https://api.geoauth.example.com/device/') as response:
    data = json.loads(response.read().decode())
    print(data)
```

**3. Python - AIOHTTP (Async)**
```python
import aiohttp
import asyncio

async def get_client_ip():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.geoauth.example.com/ip/') as response:
            data = await response.json()
            return data

# Usage
ip_data = asyncio.run(get_client_ip())
print(ip_data)
```

**4. Python - Django Integration**
```python
from django.conf import settings
import requests

def get_geo_info(request):
    # Using in Django view
    response = requests.get('https://api.geoauth.example.com/location/')
    return response.json()
```

**5. Python - Flask Integration**
```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/user-location')
def user_location():
    # Forward client info to GeoAuth API
    response = requests.get('https://api.geoauth.example.com/location/')
    return jsonify(response.json())
```

✅ **Best for**: Users who need geo-data without installing the plugin or for cross-platform applications.

# 🔐 User Registration with Geo Restriction

## 📌 Overview
GeoAuth plugin provides country-based registration restrictions, allowing you to control which countries can register users on your platform.

## ⚙️ Configuration
Add allowed countries to your `settings.py`:

```python
# settings.py
ALLOWED_COUNTRIES = ["US", "CA", "UK", "AU"]  # Country codes or names
```

## 🔄 Default Serializer
The plugin includes a default UserSerializer that handles country validation. You can find the default UserSerializer in geo_auth/serializers.py:

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError
from django.conf import settings
from .utility import get_location_from_ip, get_client_ip

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
            "name": country_name.title(),
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
        create the user without saving the confirm_password and the country if not in the model instance
        """
        validated_data.pop("confirm_password", None)
        validated_data.pop("country", None)
        user = User.objects.create_user(**validated_data)
        return user
```

## 🖥️ Default Registration View
The plugin includes a ready-to-use view for user registration:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
        
        # Return validation errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

## 🛠️ Customization Options

### ✅ Override the Serializer
User can extend the default serializer to add custom fields or validation:

```python
from geo_auth.serializers import UserSerializer

class CustomUserRegistrationSerializer(UserSerializer):
    phone_number = serializers.CharField(max_length=15, required=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["phone_number"]
        
    # Add additional validation if needed
    def validate_phone_number(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must include country code")
        return value
```

### ✅ Override the View
User can customize the registration view:

```python
from geo_auth.views import UserRegistrationView
from .serializers import CustomUserRegistrationSerializer

class CustomRegisterView(UserRegistrationView):
    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.save()
            # Additional custom logic here
            return Response({
                "message": "User registered with custom logic",
                "user": serializer.data,
                "country": serializer.validated_data.get("country")
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

## 📡 API Usage

### Registration Endpoint
```
POST /geo-auth/register/
```

### Request Body
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

### Successful Response (201 Created)
```json
{
  "message": "User registered successfully",
  "user": {
    "username": "john_doe",
    "email": "john@example.com",
    "country": {
      "name": "United States",
      "code": "US"
    }
  }
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Registration from this country is not allowed.",
  "country": {
    "name": "Restricted Country",
    "code": "RC"
  }
}
```

### Password Validation Error
```json
{
  "non_field_errors": ["Password must be at least eight characters long."]
}
```

### Email Already Exists Error
```json
{
  "email": ["This email address is already in use."]
}
```

Certainly! Here’s the license and contribution sections for your documentation:

---

## 📝 License

GeoAuth is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 🤝 Contributing

We welcome contributions to the GeoAuth plugin! If you'd like to contribute, please follow these steps:

1. **Fork the repository** on GitHub.
2. **Clone your fork** to your local machine.
   ```sh
   git clone https://github.com/shoileazeez/drf_geodata.git
   cd geo_auth
   ```
3. **Create a new branch** for your changes.
   ```sh
   git checkout -b feature/your-feature
   ```
4. **Make your changes** and **commit them**.
   ```sh
   git commit -m "Add new feature or fix"
   ```
5. **Push your changes** to your fork.
   ```sh
   git push origin feature/your-feature
   ```
6. **Open a pull request** with a description of your changes.

Please ensure your code adheres to the project's style guidelines, and add tests where appropriate. We will review your pull request and merge it once it's ready.

---
