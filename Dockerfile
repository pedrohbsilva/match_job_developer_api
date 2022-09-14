FROM python:3.8

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip3 install -r requirements.txt 

# # adicionar usuário que não é root
# RUN adduser --disabled-password myuser
# USER myuser

CMD gunicorn --bind 0.0.0.0:$PORT app