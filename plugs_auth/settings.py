"""
Plugs Auth Settings
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


MANDATORY_SETTINGS = ['SITE_RESET_VIEW', 'SITE_ACTIVATE_VIEW']
PROJECT_SETTINGS = getattr(settings, 'PLUGS_AUTH', {})


for setting in MANDATORY_SETTINGS:
    try:
        PROJECT_SETTINGS[setting]
    except KeyError:
        raise ImproperlyConfigured('Missing setting: PLUGS_AUTH[\'{0}\']'.format(setting))


plugs_auth_settings = PROJECT_SETTINGS
