FROM python:latest
LABEL authors="Borup"

COPY . /app

# Installing requirements for SpaCy
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download da_core_news_sm
RUN python -m spacy download en_core_web_sm

WORKDIR /app

CMD ["python", "main.py"]

ENTRYPOINT ["top", "-b"]