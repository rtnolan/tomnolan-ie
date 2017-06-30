FROM python:3.6-slim
MAINTAINER Tom Nolan <tomnolan95@gmail.com>

ENV INSTALL_PATH /mesh
RUN mkdir -p $INSTALL_PATH

RUN echo $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN ls

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "snakeeyes.app:create_app()"