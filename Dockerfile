FROM continuumio/anaconda3:2021.11

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt
