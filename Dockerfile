FROM python:3.8

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip3 install -r requirements.txt 

CMD flask run --host=0.0.0.0 --port=5000