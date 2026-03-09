import os

if os.getcwd() == '/app':
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config(default='postgres://localhost')
    }

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
