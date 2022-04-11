# Simple order

Simple web site to manage orders without handling payment.

## Dependencies

* python3-django
* python3-django-web-utils
* uwsgi
* uwsgi-plugin-python3

## Installation on Debian/Ubuntu

### Add systel user to run the project

``` bash
adduser --disabled-password --shell /sbin/nologin --group simple_order
```

### Clone project

``` bash
cd /home/simple_order
git clone https://github.com/sdiemer/simple_order.git
chown -R simple_order:simple_order /home/simple_order
```

### Superuser account creation

``` bash
runuser -u simple_order -- python3 /home/simple_order/simple_order/manage.py createsuperuser admin
chown -R simple_order:simple_order /home/simple_order
```
