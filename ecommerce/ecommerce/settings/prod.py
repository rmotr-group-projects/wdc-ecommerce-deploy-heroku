import os
import dj_database_url
from .base import *


ALLOWED_HOSTS = ['*']
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    '^8ai-6gb!yyg19uangdahsi8a%c=)mb0xler7%0klh1mz!^snago;91_')


# YOUR CODE HERE
