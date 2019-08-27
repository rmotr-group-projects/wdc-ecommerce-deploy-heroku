import os
import dj_database_url
from .base import *


ALLOWED_HOSTS = ['*']
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    '^8ai-6gb!yyg19uangdahsi8a%c=)mb0xler7%0klh1mz!^snago;91_')


# YOUR CODE HERE
db_from_env = dj_database_url.config()

DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
