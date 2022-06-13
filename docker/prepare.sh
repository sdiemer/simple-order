# Script to prepare docker environment
mkdir -p /opt/src/docker/data
ln -sfn /opt/src/docker/data /home/djdev/so-data

mkdir -p /opt/src/docker/data/static
ln -sfn /opt/src/simple_order/static/simple_order /opt/src/docker/data/static/
ln -sfn /usr/local/lib/python3.9/dist-packages/django/contrib/admin/static/admin /opt/src/docker/data/static/

python3 simple_order/manage.py migrate
