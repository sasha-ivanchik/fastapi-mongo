FROM python:3.10-slim-bullseye
RUN mkdir src
WORKDIR /src
COPY ./requirements.txt /src/

RUN apt-get update && apt-get install -y libpq-dev build-essential

USER root
# Install packages you need:
RUN apt-get update && apt-get install -y curl
# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID

RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend/ /src

RUN chmod -R 777 /src/starter/app.sh
