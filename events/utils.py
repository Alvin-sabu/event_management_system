# your_app/utils.py

from django.core.exceptions import PermissionDenied

def department_required(function):
    def wrap(request, *args, **kwargs):
        if not getattr(request.user, 'is_department', False):
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap
from django.core.exceptions import PermissionDenied

def admin_required(user):
    if user.is_staff or user.is_superuser:
        return True
    raise PermissionDenied

def send_prize_notification_emails(winners, event):
    # Implement the email sending logic here
    pass


import requests

import requests

def get_weather(city):
    API_KEY = '5559494dbb4c4740be4f78a0679f2db1'  # Replace with your actual Weatherbit API key
    url = f'https://api.weatherbit.io/v2.0/current?city={city}&key={API_KEY}&units=M'  # 'M' for metric (Celsius)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        weather_data = response.json()

        if weather_data.get('data'):
            weather_info = weather_data['data'][0]
            return {
                'temperature': weather_info['temp'],
                'description': weather_info['weather']['description'],
                'icon': weather_info['weather']['icon']
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        # This will catch any requests-related errors (e.g., connection errors, timeouts, HTTP errors)
        print(f"Error fetching weather data: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        # This will catch any errors related to unexpected data structure
        print(f"Error processing weather data: {e}")
        return None