FROM python:3.11.9-slim-bullseye
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y binutils libproj-dev gdal-bin build-essential python3-dev curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem \
    -o /etc/ssl/certs/aws-rds-global-bundle.pem
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["bash", "docker-entrypoint.sh"]
