# this file is used to identify which settings file to load based on the selected MY_ENV in .env

from .base import *

if MY_ENV in ['local', 'develop']:
    from .develop import *
elif MY_ENV in ['production']:
    from .production import *
else:
    raise ValueError("The environment variable MY_ENV should be set in .env as one of: local, develop, or production")