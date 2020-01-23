FROM python:3.7-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN apt-get update && \
    apt-get install make && \
    DEBIAN_FRONTEND='noninteractive' apt-get install virtualenv -y && \
    pip install -r requirements.txt

CMD python run.py