FROM python:3.12.16-slim-trixie

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# WARNING: the GIS packages (binutils libproj-dev gdal-bin) are not used by the project (no django.contrib.gis).
# gdal pulls in libmariadb3, mariadb-common and libxml2, which are the only CRITICAL findings in trivy
# (no Debian fix available yet). Dropping them brings the image to 0 CRITICAL.
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y binutils libproj-dev gdal-bin curl \
 && rm -rf /var/lib/apt/lists/*

# emSign/eMudhra incident: Debian's ca-certificates still ships the roots that upstream (Mozilla/certifi) removed.
# Blacklist them in the OS trust store (Debian-supported "!" syntax). Remove once Debian ships the fixed ca-certificates.
RUN sed -i -E 's#^(mozilla/emSign_(Root_CA_-_C1|ECC_Root_CA_-_C3)\.crt)$#!\1#' /etc/ca-certificates.conf \
 && update-ca-certificates --fresh

WORKDIR /code

COPY requirements.txt /code/

# pip >= 26.2.2 (emSign incident). The base image's old pip still trusts the compromised emSign roots, so the
# upgrade itself is pinned by sha256 (pip-26.3-py3-none-any.whl from PyPI): a tampered download fails the hash check.
# git is only needed to install the django_survey_monkey VCS dependency.
RUN apt-get update \
 && apt-get install -y git \
 && python -m pip install --no-cache-dir "pip @ https://files.pythonhosted.org/packages/07/25/ee8c38ae72d66b844ce8eb9711ba905dba21ca1a8a0c960057c41cd23337/pip-26.3-py3-none-any.whl#sha256=f3b60b20ffaadd4415ed7957212a38ac63fa4c5fa375bd0f4a797777940fad13" \
 && pip install -r requirements.txt \
 && apt-get purge -y git \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

COPY . /code/

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
