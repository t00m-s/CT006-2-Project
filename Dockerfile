FROM  python:3.9-slim-bullseye
WORKDIR /ct0006
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY backend /ct0006/backend
COPY frontend /ct0006/frontend
ENV FLASK_APP=app
CMD ["python", "backend/app.py"]