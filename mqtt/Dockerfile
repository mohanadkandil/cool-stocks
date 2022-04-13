FROM python:3.9.6

WORKDIR /thndr-mqtt-client

COPY . .

RUN pip install paho-mqtt
RUN pip install requests-futures
RUN pip install pydantic

CMD ["python", "./main.py"]

