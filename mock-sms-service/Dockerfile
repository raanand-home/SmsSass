FROM python:2.7
RUN mkdir /app/
RUN apt-get update && apt-get install dumb-init
WORKDIR /app/
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD app.py app.py
EXPOSE 5002
CMD dumb-init python app.py
