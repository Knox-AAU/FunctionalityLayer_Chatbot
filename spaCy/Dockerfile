# LÆS README FOR AT FORSTÅ DOCKERFILEN

FROM ubuntu:latest

FROM python:3.11

LABEL authors="Borup"

COPY . /app

# Installing requirements for SpaCy
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download da_core_news_md

WORKDIR /app

CMD ["python", "main.py"]
