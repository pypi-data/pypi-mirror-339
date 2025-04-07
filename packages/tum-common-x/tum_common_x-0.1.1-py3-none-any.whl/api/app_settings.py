# my_django_base/app_settings.py
from django.conf import settings

# Default settings that can be overridden
DEFAULTS = {
    'ENABLE_FEATURE_X': True,
    'MAX_ITEMS_PER_PAGE': 25,
    'CACHE_TIMEOUT': 3600,
    'ALLOWED_EXTENSIONS': ['.jpg', '.png', '.pdf'],
}

# Function to get settings with fallbacks to defaults
def get_setting(name):
    app_settings = getattr(settings, 'MY_DJANGO_BASE', {})
    return app_settings.get(name, DEFAULTS.get(name))

# Usage example:
# from my_django_base.app_settings import get_setting
# cache_timeout = get_setting('CACHE_TIMEOUT')