from mamaKovasi.settings.base import *

DEBUG=False

STATIC_ROOT = os.path.join(BASE_DIR, "static")

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
