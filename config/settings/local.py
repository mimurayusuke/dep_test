from .base import *

SECRET_KEY = '0=qt9!wc&msa%oqq-vg@bug!lpf!)e2!j%y7&v(28d9d2(9o27'

DEBUG = True

ALLOWED_HOSTS = []

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]
#開発環境でcollectstaticはしないので必要ない。
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')