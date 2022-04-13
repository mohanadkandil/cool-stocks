FROM python:3.9.6-slim-buster

WORKDIR /thndr-database

COPY . .

RUN pip install pipenv
RUN pipenv install --system

EXPOSE 80

CMD ["python", "app/main.py"]