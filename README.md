# Simple order

Simple web site to manage orders without handling payment.

## Dependencies

* python3-django
* uwsgi
* uwsgi-plugin-python3

## Installation on Debian/Ubuntu

### Add systel user to run the project

``` bash
adduser --disabled-password --shell /usr/sbin/nologin simple-order
```

### Clone project

``` bash
cd /opt
git clone --recursive https://github.com/sdiemer/simple-order.git
chown -R simple-order: /opt/simple-order
ln -s /opt/simple-order/simple_order/scripts/simple-order.service /lib/systemd/system/
ln -s /opt/simple-order/simple_order/scripts/control.py /usr/local/bin/simple-order-control
```

### Init project

``` bash
mkdir -p /home/simple-order/so-data/private
secret_key=$(tr -dc 'a-z0-9!@#$%^&*\-_=+(){}[]' < /dev/urandom | head -c50)
echo "SECRET_KEY = '$secret_key'" >> "/home/simple-order/so-data/private/settings_override.py"
chown -R simple-order: /home/simple-order
chmod 700 /home/simple-order/so-data/private
runuser -u simple-order -- python3 /opt/simple-order/simple_order/manage.py migrate
```

### Superuser account creation

``` bash
runuser -u simple-order -- python3 /opt/simple-order/simple_order/manage.py createsuperuser --username admin
```
