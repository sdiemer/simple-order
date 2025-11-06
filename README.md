# Simple order

Simple web site to manage orders without handling payment.

## OS dependencies

* uwsgi
* uwsgi-plugin-python3

## Installation on Debian/Ubuntu

### First initialization

``` bash
mkdir -p /opt/simple-order
cd /opt/simple-order
git clone --recursive https://github.com/sdiemer/simple-order.git repo
bash /opt/simple-order/repo/deployment/setup.sh
```

### Update

``` bash
bash /opt/simple-order/repo/deployment/setup.sh
```

### backup database

```bash
simple-order-control manage dump
```

### Superuser account creation

``` bash
simple-order-control manage createsuperuser --username admin
```
