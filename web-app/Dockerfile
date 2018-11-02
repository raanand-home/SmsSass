FROM python:2.7
RUN mkdir /app/
RUN apt-get update && apt-get install dumb-init
WORKDIR /app/
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
CMD dumb-init python app.py
