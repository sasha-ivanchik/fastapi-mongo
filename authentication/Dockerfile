FROM python:3.10-slim-bullseye

RUN mkdir src
WORKDIR /src
COPY ./requirements-auth.txt /src/

USER root
RUN apt-get update && apt-get install -y curl
USER $NB_UID

RUN pip install --no-cache-dir -r requirements-auth.txt

COPY ./authentication/ /src

RUN chmod a+x /src/starter/app.sh
