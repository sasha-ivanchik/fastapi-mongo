FROM python:3.10-slim-bullseye

RUN mkdir src
WORKDIR /src
COPY ./requirements-auth.txt /src/

RUN apt-get update && apt-get install -y libpq-dev build-essential
USER root
# Install packages you need:
RUN apt-get update && apt-get install -y curl
# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
RUN pip install --no-cache-dir -r requirements-auth.txt

COPY ./authentication/ /src

RUN chmod a+x /src/starter/app.sh
