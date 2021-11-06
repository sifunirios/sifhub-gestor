from .base import *

# Disable Django’s static file handling and allow WhiteNoise to take over
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')

INSTALLED_APPS += [
    # ...
]
