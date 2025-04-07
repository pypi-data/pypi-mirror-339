import IP2Location
import iso3166
import pycountry
import requests
from ipware import get_client_ip
from timezonefinder import TimezoneFinder
from user_agents import parse
import os
from django.conf import settings
import os
from importlib.resources import files
import os
from pathlib import Path

try:
    # First try the package resource approach (works when installed)
    package_path = files('geo_auth')
    database_path = str(package_path.joinpath('iplite_database/IP2LOCATION-LITE-DB11.BIN'))
    asn_database_path = str(package_path.joinpath('iplite_database/IP2LOCATION-LITE-ASN.BIN'))
except (ImportError, ModuleNotFoundError):
    # Fallback for development environment
    current_dir = Path(__file__).resolve().parent
    database_path = str(current_dir / 'iplite_database' / 'IP2LOCATION-LITE-DB11.BIN')
    asn_database_path = str(current_dir / 'iplite_database' / 'IP2LOCATION-LITE-ASN.BIN')

# Initialize databases with the correct paths
database = IP2Location.IP2Location(database_path)
asn_database = IP2Location.IP2Location(asn_database_path)
GEONAMES_USERNAME = settings.GEONAMES_USERNAME
if not GEONAMES_USERNAME:
    raise ValueError("GeoNames username not set. Please configure the GEONAMES_USERNAME environment variable.")
tf = TimezoneFinder()

def get_currency_from_country(country_code):
    """Fetches currency code based on country code."""
    try:
        country = pycountry.countries.get(alpha_2=country_code.upper())
        if not country:
            return None
        
        # Get country info using iso3166
        country_info = iso3166.countries_by_alpha2.get(country_code.upper())
        if not country_info:
            return None
        
        # Get currency info
        currency = pycountry.currencies.get(numeric=country_info.numeric)
        return currency.alpha_3 if currency else None
    except Exception:
        return None

def get_country_info(country_code):
    """Fetches country info based on country code"""
    
    url = f"http://api.geonames.org/countryInfoJSON?country={country_code}&username={GEONAMES_USERNAME}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # print(data)
        if "geonames" in data and data["geonames"]:
            return data["geonames"][0]  # Return the first country match
        else:
            return "No data found for this country code."
    else:
        return f"Error: {response.status_code}"

def get_timezone_name(latitude, longitude):
    """Finds the timezone from latitude and longitude."""
    try:
        # Convert to float in case the values are strings
        latitude = float(latitude)
        longitude = float(longitude)

        # Validate coordinates
        if latitude == 0.0 and longitude == 0.0:
            return "Unknown (Invalid Coordinates: 0.0, 0.0)"

        # Primary timezone lookup
        timezone = tf.timezone_at(lat=latitude, lng=longitude)

        # Fallback method if the primary lookup fails
        if not timezone:
            timezone = tf.closest_timezone_at(lat=latitude, lng=longitude)

        return timezone if timezone else "Unknown (No Matching Timezone)"
    except ValueError:
        return "Unknown (Invalid Coordinate Values)"
    except Exception as e:
        return f"Unknown (Error: {str(e)})"


def get_location_from_ip(ip_address):
    "Fetches user location data based on IP address"
    try:
        #Look up the IP address
        response = database.get_all(ip_address)
        asn_response = asn_database.get_all(ip_address)
        latitude = response.latitude
        longitude = response.longitude

        # Convert timezone offset to a human-readable name
        timezone_name = get_timezone_name(latitude, longitude)
        
        location_data = {
            'country_code': response.country_short,
            'country': response.country_long,
            'region': response.region,
            'city': response.city,
            'latitude': response.latitude,
            'longitude': response.longitude,
            'zip_code': response.zipcode,
            'timezone': timezone_name,
            'asn': asn_response.asn,
            
        }

        return location_data
    except Exception as e:
        return {'error': str(e)}

def get_ip(request):
        """Fetches the real public IP address of the request."""
        ip_address, is_routable = get_client_ip(request)

        if not ip_address:
            ip_address = "Unknown IP"
        elif not is_routable:
            ip_address = "Private Network IP"

        return ip_address 
    
def get_my_device_info(request):
        """ Fetches the Device info of the request"""
        user_agent_string = request.headers.get('User-Agent', '')
        user_agent = parse(user_agent_string)
        device_info = {
            "device": user_agent.device.family or "Unknown",
            "browser": user_agent.browser.family or "Unknown",
            "os": user_agent.os.family or "Unknown",
            "is_mobile": user_agent.is_mobile,
            "is_tablet": user_agent.is_tablet,
            "is_pc": user_agent.is_pc,
            }
        return device_info