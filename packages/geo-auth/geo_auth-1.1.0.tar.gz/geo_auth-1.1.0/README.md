# 🌐 GeoAuth Plugin Documentation

## 📌 Overview
**GeoAuth** is a Django plugin that adds powerful geo-location and user analytics capabilities to your web app. It allows you to:

1️⃣ Retrieve visitor **IP addresses**  
2️⃣ Get detailed **device information** (browser, OS, etc.)  
3️⃣ Fetch **geo-location data** (country, city, region, lat, long)  
4️⃣ Access **country details** (languages, timezone, currency)  
5️⃣ **Restrict user registration** based on country

---

## 🚀 Installation

### Via pip
```bash
pip install geo-auth
```

### From Source
```bash
git clone https://github.com/shoileazeez/drf_geodata.git
cd geo_auth
pip install -r requirements.txt
```

---

## ⚙️ Setup & Configuration

### 1️⃣ Add Plugin to Installed Apps
In your `settings.py`:
```python
INSTALLED_APPS = [
    # other apps...
    'geo_auth',
]
```

### 2️⃣ Run Migrations
```bash
python manage.py migrate
```

### 3️⃣ Enable GeoAuth Middleware
To automatically enrich every request with geo and device data:
```python
MIDDLEWARE = [
    # other middleware...
    'geo_auth.middleware.GeoAuthMiddleware',
]
```

### 4️⃣ Register Plugin URLs
In your project’s `urls.py`:
```python
from django.urls import path, include

urlpatterns = [
    # other URLs...
    path('geo_auth/', include('geo_auth.urls')),
]
```

---

## 🌍 Geo Data Configuration

### 🔑 IP2Location Token
1. Register at [IP2Location Lite](https://lite.ip2location.com/) and obtain your token.
2. Add it to your environment variables:
```bash
export TOKEN="your_api_token"
```
3. Access it in `settings.py`:
```python
import os
TOKEN = os.getenv("TOKEN")
```

---

### 🌎 GeoNames Username
1. Sign up at [GeoNames](https://www.geonames.org/login).
2. Add your GeoNames username to your environment:
```bash
export GEONAMES_USERNAME="your_username"
```
3. Retrieve it in `settings.py`:
```python
GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")
```

---

## 🛠️ Development Notice: IP Address Resolution

🔍 **Important for Local Development**

If you're testing locally (e.g., on `127.0.0.1` or `localhost`), the plugin will only capture **private IPs**, not public ones. To test with real public IP addresses during development:

> 💡 Use [ngrok](https://ngrok.com/) to expose your local server to the internet.

### Example:
```bash
ngrok http 8000
```
Then visit the public URL provided by ngrok (e.g., `https://1234.ngrok.io`) to trigger real geo-data collection.

✅ In **production**, this is not required — real IP addresses will be captured automatically.

---


## 🔌 Usage Options

### Option 1: Automatic Middleware Enrichment
```python
from django.http import JsonResponse
def example_view(request):
    return JsonResponse({
        "client_ip": request.ip_address,
        "location_data": {
            "location": request.location_data,
            "country_info": request.country_info,
            "currency": request.currency
        },
        "device_info": request.device_info,
    })
```

---

### Option 2: API Views with Middleware
```python
from rest_framework.response import Response
from rest_framework.decorators import api_view
@api_view(["GET"])
def get_client_ip_auto(request):
    return Response({"client_ip": request.ip_address})

@api_view(["GET"])
def location_info(request):
    return Response({"location": request.location_data})

@api_view(["GET"])
def get_client_device_info(request):
    return Response({"device_info": request.device_info})
```

---

**Option 3: Utility Function Calls (No Middleware)** section with both **standard Django views** and **Django REST Framework function-based views**:

---

### ✅ Option 3: Utility Function Calls (No Middleware)

You can directly use GeoAuth’s utility functions in your views without enabling middleware.

#### 🔹 Example – Standard Django Views

```python
from geo_auth.utility import get_ip, get_location_from_ip, get_my_device_info, get_country_info
from django.http import JsonResponse

def example_view_ip_device(request):
    return JsonResponse({
        "ip": get_ip(request),
        "device": get_my_device_info(request),
    })

def example_view_country_info(request):
    country_code = "NG"
    return JsonResponse({
        "country_info": get_country_info(country_code),
    })

def example_view_location_info(request):
    ip_address = "102.89.22.52"
    return JsonResponse({
        "location_info": get_location_from_ip(ip_address),
    })
```

---

#### 🔹 Example – Django REST Framework Function-Based Views

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geo_auth.utility import get_ip, get_location_from_ip, get_my_device_info, get_country_info

@api_view(["GET"])
def get_ip_and_device(request):
    return Response({
        "ip": get_ip(request),
        "device": get_my_device_info(request),
    })

@api_view(["GET"])
def get_country_details(request):
    country_code = "NG"  # Or get from query params: request.GET.get("country")
    return Response({
        "country_info": get_country_info(country_code),
    })

@api_view(["GET"])
def get_location_by_ip(request):
    ip_address = "102.89.22.52"  # Or get from query params: request.GET.get("ip")
    return Response({
        "location_info": get_location_from_ip(ip_address),
    })
```

### Option 4: Built-In API Endpoints
After registering plugin URLs (`/geo_auth/`), you get these endpoints:

| Endpoint | Description |
|---------|-------------|
| `GET /geo_auth/ip/` | Returns client IP |
| `GET /geo_auth/device/` | Returns device info |
| `GET /geo_auth/location/` | Returns geo-location data |

---


### 📡 Option 5: Hosted API (No Installation Needed)

If you prefer not to install GeoAuth, you can use our hosted API service.

#### **Hosted API Endpoints**:
- `GET https://drf-geodata.onrender.com/ip/` — Returns client IP
- `GET https://drf-geodata.onrender.com/device/` — Returns device info
- `GET https://drf-geodata.onrender.com/location/` — Returns geo-location data

---

### 🔹 Example – Using Django's `requests` library:

```python
import requests
from django.http import JsonResponse

def get_client_ip(request):
    url = "https://drf-geodata.onrender.com/ip/"
    response = requests.get(url)
    return JsonResponse(response.json())

def get_device_info(request):
    url = "https://drf-geodata.onrender.com/device/"
    response = requests.get(url)
    return JsonResponse(response.json())

def get_location_data(request):
    url = "https://drf-geodata.onrender.com/location/"
    response = requests.get(url)
    return JsonResponse(response.json())
```

In this example, the Django view makes a `GET` request to the hosted GeoAuth API and returns the response in the view. The data is returned as a JSON response to the client.

---

### 🔹 Example – Using Python's `requests` library (External Usage):

```python
import requests

def get_client_ip():
    url = "https://drf-geodata.onrender.com/ip/"
    response = requests.get(url)
    return response.json()

def get_device_info():
    url = "https://drf-geodata.onrender.com/device/"
    response = requests.get(url)
    return response.json()

def get_location_data():
    url = "https://drf-geodata.onrender.com/location/"
    response = requests.get(url)
    return response.json()
```

This example uses the Python `requests` library to send `GET` requests to the hosted GeoAuth API, which can be executed in an external script or service.

---

---

## 🔐 Country-Based User Registration Restriction

### Step 1: Allowed Countries

In `settings.py`:
```python
ALLOWED_COUNTRIES = ["US", "CA", "UK", "AU"]
```

### Step 2: Use the Provided `UserSerializer`

Handles:
- Country validation via IP
- Duplicate email check
- Password confirmation

---

### Step 3: Default Registration View
```python
from geo_auth.views import UserRegistrationView

class RegisterView(UserRegistrationView):
    pass  # Uses default UserSerializer behavior
```

---

### 🧩 Customizing the Default Serializer

You can override the default serializer to extend user fields (e.g., adding `phone_number`).

```python
from geo_auth.serializers import UserSerializer
from rest_framework import serializers

class CustomUserRegistrationSerializer(UserSerializer):
    phone_number = serializers.CharField(max_length=15, required=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["phone_number"]

    def validate_phone_number(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must include country code")
        return value
```

---

### 🛠 Using Your Custom Serializer in Views

```python
from geo_auth.views import UserRegistrationView
from .serializers import CustomUserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status

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

---

## 📡 API Usage

### Registration Endpoint
```
POST /geo_auth/register/
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

### Email Already Exists and Username Error
```json
{
    "username": [
        "A user with that username already exists."
    ],
    "email": [
        "This email address is already in use."
    ]
}
```

---

## ✅ Summary

| Feature | Works Out of the Box |
|--------|-----------------------|
| Django | ✅ |
| Hosted API | ✅ |
| Local Dev (Real IPs) | 🔄 Requires `ngrok` |
| Public Deployment | ✅ Fully functional |

---

## 📞 Support & Contributions

Need help or want to contribute? Feel free to [open an issue](https://github.com/shoileazeez/drf_geodata/issues) or submit a pull request. We welcome improvements and feedback!

---
