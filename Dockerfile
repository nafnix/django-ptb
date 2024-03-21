# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11
FROM library/python:${PYTHON_VERSION}-bookworm AS builder

ARG PYPI_MIRROR=https://pypi.org/simple
WORKDIR /tmp
COPY ./pyproject.toml ./pdm.lock ./
RUN <<EOT
    pip install pdm --upgrade --no-cache-dir -i ${PYPI_MIRROR}
    pdm export --without-hashes -o ./requirements.txt --prod -v
EOT


FROM library/python:${PYTHON_VERSION}-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

ARG PYPI_MIRROR=https://pypi.org/simple
COPY --from=builder /tmp/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade --no-cache-dir -i ${PYPI_MIRROR} -r /tmp/requirements.txt

ARG USER=django
ENV DJANGO_STATIC_ROOT=/var/www/static \
    DJANGO_BASE_DIR=/website

COPY . ${DJANGO_BASE_DIR}
RUN <<EOT
    useradd -m -d ${DJANGO_BASE_DIR} -s /bin/bash ${USER}
    mkdir -p ${DJANGO_STATIC_ROOT} ${DJANGO_BASE_DIR}
    chown -R ${USER}:${USER} ${DJANGO_BASE_DIR} ${DJANGO_STATIC_ROOT}
EOT


USER ${USER}
WORKDIR ${DJANGO_BASE_DIR}
RUN <<EOT
    chmod +x entrypoint.sh
EOT

ENTRYPOINT [ "bash", "./entrypoint.sh" ]
