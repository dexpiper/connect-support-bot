FROM python:3.11-slim-bookworm AS drugbot

RUN apt-get update && apt-get install -y -q \
        python3                             \
        python3-pip                         \
&& rm -rf /var/lib/apt/lists/*
ADD . drugbot
WORKDIR /drugbot
RUN pip --no-cache-dir install -r requirements.txt
ENTRYPOINT python3 /drugbot/main.py
