# every docker instruction is a layer
FROM python:3.10-slim-bullseye  

RUN app-get update\
    && apt-get install -y --no-install-recommends --no-install-suggests\
    build-essential default-libmysqlclient-dev\
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]

# draw layer illustration for docker

# pip3 freeze > requirements.txt
