FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH /app

ENV TZ=Asia/Jakarta

CMD [ "python", "./app.py" ]