from .base import *

SECRET_KEY = '0=qt9!wc&msa%oqq-vg@bug!lpf!)e2!j%y7&v(28d9d2(9o27'

DEBUG = False

ALLOWED_HOSTS = ['yskexe.com']

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]
#collectstaticコマンドで静的ファイルを集める本番環境Webサーバ（nginx）のディレクトリを指定。
STATIC_ROOT = '/usr/share/nginx/html/static'

#本番環境で利用するWebサーバ nginxのディレクトリにメディアファイルを集める。
MEDIA_URL = '/media/'
MEDIA_ROOT = '/usr/share/nginx/html/media'