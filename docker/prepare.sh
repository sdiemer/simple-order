# Script to prepare docker environment
mkdir -p /opt/src/docker/data
ln -sfn /opt/src/docker/data /home/djdev/so-data

mkdir -p /opt/src/docker/data/static
ln -sfn /opt/src/simple_order/static/simple_order /opt/src/docker/data/static/
ln -sfn /usr/local/lib/python3.9/dist-packages/django/contrib/admin/static/admin /opt/src/docker/data/static/

mkdir -p /opt/src/docker/data/private
if [ ! -f /opt/src/docker/data/private/settings_override.py ]; then
	echo '# Local settings
DEBUG = True
DEBUG_TOOLBAR = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
' > /opt/src/docker/data/private/settings_override.py
fi

python3 simple_order/manage.py migrate
