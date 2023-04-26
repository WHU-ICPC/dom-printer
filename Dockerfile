FROM python:3.9.16-bullseye

RUN mkdir -p /data/apps/dom-printer
WORKDIR /data/apps/dom-printer

COPY . .
RUN pip install -r requirements-server.txt
ENTRYPOINT ["python", "server.py"]