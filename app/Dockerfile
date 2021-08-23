FROM python:3.7

ENV PYTHONIOENCODING utf-8

WORKDIR /app

COPY . .

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uwsgi","--ini","uwsgi.ini"]
