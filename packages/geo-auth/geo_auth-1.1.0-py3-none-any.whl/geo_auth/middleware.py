from .utility import (get_country_info, get_currency_from_country, get_ip,
                      get_location_from_ip, get_my_device_info)


class GeoAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract ip_address , device info and client location data from request
        ip_address = get_ip(request)
        location_data = get_location_from_ip(ip_address) if ip_address else {}
        device_info = get_my_device_info(request)

        # Extract country and fetch currency
        country_code = location_data.get("country_code")
        currency = get_currency_from_country(country_code) if country_code else None
        country_info = get_country_info(country_code) if country_code else None

        # Attach data to request
        request.ip_address = ip_address
        request.location_data = location_data
        request.currency = currency
        request.country_info = country_info
        request.device_info = device_info

        return self.get_response(request)
