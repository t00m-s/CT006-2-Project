FROM python:3.9-slim-bullseye

WORKDIR /app

COPY ./flask/code /app
COPY ./flask/requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["flask", "run","--host=0.0.0.0"]
