FROM python:3.10

RUN mkdir src
WORKDIR /src
COPY ./requirements.txt /src/

RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt

COPY ./authentication/ /src

RUN chmod a+x /src/starter/app.sh
