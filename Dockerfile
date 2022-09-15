FROM python:3.9



WORKDIR /app

COPY . /app

RUN apt-get update

RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 3306


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008","--reload"]