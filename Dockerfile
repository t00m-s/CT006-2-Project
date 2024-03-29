FROM python:3.9-slim-bullseye
WORKDIR /app
COPY ./code /app
RUN pip install --no-cache-dir -r requirements.txt
