FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION ignore
WORKDIR /app
COPY . /app

RUN pip install --no-cache --upgrade pip \
 && pip install --no-cache /app \
 && addgroup --system app && adduser --system --group app \
 && mkdir -p /opt/shell_gpt \
 && mkdir -p /home/app \
 && chown -R app:app /opt/shell_gpt /home/app

USER root

VOLUME /tmp/shell_gpt

ENTRYPOINT ["sgpt"]
