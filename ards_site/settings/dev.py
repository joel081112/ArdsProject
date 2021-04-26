from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r$m8_w8m#&cf6cw(#%lx=#fn3^(m2ndtiusfz&05ft9a&1dqv*'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# THIS WAS CONSOLE FOR DEVELOPMENT PURPOSES FOR SIGN UP VERIFICATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
    'jquery',
]

MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
    '172.17.0.1',
]

try:
    from .local import *
except ImportError:
    pass
