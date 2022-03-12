# python3.9のイメージをダウンロード
FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /var/www

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
COPY ./docker/app/entrypoint.sh /bin/entrypoint.sh

RUN apt-get update && \
    apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN echo 'PATH=$HOME/.poetry/bin:$PATH' >> ~/.bashrc
RUN . /root/.profile && \
    poetry config virtualenvs.in-project true && \
    poetry install;


# uvicornのサーバーを立ち上げる
ENTRYPOINT ["/root/.poetry/bin/poetry","run","uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8888","--reload"]
