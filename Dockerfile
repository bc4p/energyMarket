FROM python:3.10.12-alpine

COPY . /
WORKDIR /


RUN apk add --no-cache g++

RUN pip install -e .
CMD ["python", "redisConnector_gsy.py"]
