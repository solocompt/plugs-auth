"""
Plugs Auth Settings
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


MANDATORY_SETTINGS = ['RESET_VIEW']
PROJECT_SETTINGS = getattr(settings, 'PLUGS_AUTH', {})

for setting in MANDATORY_SETTINGS:
    try:
        PROJECT_SETTINGS[setting]
    except KeyError:
        raise ImproperlyConfigured('Missing setting: PLUGS_AUTH[\'{0}\']'.format(setting))

DEFAULTS = {
    'USER_ENDPOINT': 'users',
    'REQUIRE_ACTIVATION': True
}

for setting in DEFAULTS.keys():
    if setting not in PROJECT_SETTINGS:
        PROJECT_SETTINGS[setting] = DEFAULTS[setting]

# conditional settings, only required if something, something...
if PROJECT_SETTINGS['REQUIRE_ACTIVATION'] and 'ACTIVATE_VIEW' not in PROJECT_SETTINGS:
    raise ImproperlyConfigured('Missing ACTIVATE_VIEW. This setting is required if REQUIRE_ACTIVATION is True')

plugs_auth_settings = PROJECT_SETTINGS
