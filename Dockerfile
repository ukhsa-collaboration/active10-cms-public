FROM python:3.15.0rc1-slim-bookworm

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y binutils libproj-dev gdal-bin build-essential python3-dev curl

WORKDIR /code

COPY requirements.txt /code/

RUN apt-get update && \
    apt-get install -y git && \
    pip install -r requirements.txt && \
    apt-get purge -y git && \
    apt-get autoremove -y

COPY . /code/

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
