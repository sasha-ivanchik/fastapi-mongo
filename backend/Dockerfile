# ====================================================================
# =========================PREP STAGE=================================
# ====================================================================
FROM python:3.10-alpine as builder

WORKDIR /src

COPY ./requirements.txt /src/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /src/wheels -r requirements.txt

# ====================================================================
# =========================MAIN STAGE=================================
# ====================================================================
FROM python:3.10-slim-bullseye
WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Switch to ROOT to install curl for health check
USER root
# Install packages you need + curl:
RUN apt-get update && apt-get install -y curl
# Switch back to avoid accidental container runs as root
USER $NB_UID
RUN pip install --upgrade pip

COPY --from=builder /src/wheels /wheels
COPY --from=builder /src/requirements.txt /
RUN pip install --no-cache /wheels/*

COPY ./backend/ /src
RUN chmod -R 777 /src/starter/app.sh