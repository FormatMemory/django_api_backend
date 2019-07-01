from .base import *


DEBUG = False

INTERNAL_IPS = [
    '127.0.0.1',
]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'xxx',
#         'USER': 'xxx',
#         'PASSWORD': 'xxx',
#         'HOST': 'xxx.xxx.xxx.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': os.environ.get('DB_PORT'),
        'default-character-set': 'utf8mb4',
        'OPTIONS': {
            # Tell MySQLdb to connect with 'utf8mb4' character set
            'charset': 'utf8mb4',
        },
    }
}
