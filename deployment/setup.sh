#!/bin/bash
if [[ $(id -u) != "0" ]]; then
    echo "This script must be run as root"
    exit 1
fi

set -e
set -x

# Create app user
if ! id -u simple-order; then
	adduser --system --group --shell /usr/sbin/nologin --home /opt/simple-order/data simple-order
fi

# Clean temp files and update repository
cd /opt/simple-order/repo
find . -name *.pyc -type f -delete
find . -name __pycache__ -type d -delete
git fetch --recurse-submodules --all
git reset --hard origin/main
git pull --recurse-submodules

# Check virtual env
if ! test -d /opt/simple-order/venv; then
	python3 -m venv /opt/simple-order/venv
fi
/opt/simple-order/venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel
/opt/simple-order/venv/bin/pip install --no-cache-dir --editable '.'

# Main entry point
ln -sfn /opt/simple-order/venv/bin/simple-order-control /usr/local/bin/simple-order-control

# Init settings file
mkdir -p /opt/simple-order/data/private
if ! grep SECRET_KEY /opt/simple-order/data/private/settings_override.py; then
	secret_key=$(tr -dc 'a-z0-9!@#$%^&*\-_=+(){}[]' < /dev/urandom | head -c50)
	echo "SECRET_KEY = '${secret_key}'" >> /opt/simple-order/data/private/settings_override.py
	echo "Secret key generated."
fi
if ! grep SITE_DOMAIN /opt/simple-order/data/private/settings_override.py; then
	echo "SITE_DOMAIN = 'simple-order'" >> /opt/simple-order/data/private/settings_override.py
	echo "Site domain added to settings."
fi

# Ensure files ownership and permissions
chown -R simple-order: /opt/simple-order/data
chown simple-order:www-data /opt/simple-order/data
chmod 700 /opt/simple-order/data/private

# Database update
/opt/simple-order/venv/bin/simple-order-control manage dump
/opt/simple-order/venv/bin/simple-order-control manage migrate

# Systemd service
ln -sfn /opt/simple-order/repo/deployment/simple-order.service /lib/systemd/system/simple-order.service
systemctl enable simple-order
systemctl restart simple-order

# Nginx configuration link
site_domain=$(grep SITE_DOMAIN /opt/simple-order/data/private/settings_override.py | awk '{print $2}' FS='=' | tr -d "' \"")
sed -i "s/server_name vhost-domain;/server_name ${site_domain};/g" /opt/simple-order/repo/deployment/nginx.conf
ln -sfn /opt/simple-order/repo/deployment/nginx.conf /etc/nginx/sites-available/simple-order.conf
ln -sfn ../sites-available/simple-order.conf /etc/nginx/sites-enabled/simple-order.conf
if ! test -f /etc/nginx/conf.d/ssl.conf; then
	echo 'ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;' > /etc/nginx/conf.d/ssl.conf
	echo 'ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;' >> /etc/nginx/conf.d/ssl.conf
fi
nginx -t
systemctl reload nginx


echo -e "    \033[92m[ OK ]\033[0m"
exit 0
