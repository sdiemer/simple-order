FROM debian:trixie

RUN apt update
RUN apt install -y make git procps sudo ca-certificates nginx ssl-cert uwsgi uwsgi-plugin-python3 python3-venv munin munin-node

ENV VIRTUAL_ENV="/opt/simple-order/venv"
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

ARG DOCKER_WORK_DIR
RUN mkdir -p ${DOCKER_WORK_DIR}
WORKDIR ${DOCKER_WORK_DIR}

RUN mkdir -p /opt/simple-order
RUN ln -s ${DOCKER_WORK_DIR} /opt/simple-order/repo
RUN ln -s ${DOCKER_WORK_DIR}/data /opt/simple-order/data

# Nginx
RUN echo 'ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;' > /etc/nginx/conf.d/ssl.conf
RUN echo 'ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;' >> /etc/nginx/conf.d/ssl.conf
RUN ln -s /opt/simple-order/repo/deployment/nginx.conf /etc/nginx/sites-enabled/app.conf

COPY pyproject.toml pyproject.toml
COPY simple_order simple_order
RUN pip install --no-cache-dir --editable '.[dev]'

# Add user matching local uid/gid
ARG USER_UID
ARG USER_GID
RUN groupadd --gid ${USER_GID} simple-order
RUN useradd --uid ${USER_UID} --gid ${USER_GID} --system --shell /usr/sbin/nologin --home /opt/simple-order/data simple-order
RUN echo "simple-order ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER simple-order
EXPOSE 443
ENTRYPOINT ["/bin/make"]
