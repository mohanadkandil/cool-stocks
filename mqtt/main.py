from paho.mqtt import client as mqtt_client
import time
import json
import os 

from requests_futures.sessions import FuturesSession

import schemas

db_url = os.environ.get('DB_URL')
db_hostname = f'http://{db_url}'
session = FuturesSession()

vernemq_hostname = os.environ.get('VERNEMQ_HOSTNAME')
broker = vernemq_hostname
port = 1883
topic = "thndr-trading"
client_id = 'thndr-topic-client'

def cmqtt() -> mqtt_client:
    def onconn(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker Successfully!")
            client.subscribe(topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.onconn = onconn
    return client
def save_stock_db(requestBody: schemas.StockCreate):
    # Update Stock
    payload = {
        **requestBody,
        'id': requestBody['stock_id']
    }
    url = 'stock/'
    try:
        response = session.put(f'{db_hostname}/db/{url}', json=payload)
        res = response.result()
    except Exception as err:
        print('db error ... ', err)
        return
    if not res.json():
    # If stock can NOT be updated --> Add Stock to DB
        payload = {
            **requestBody,
            'id': requestBody['stock_id'],
            'highestPrice': requestBody['price'],
            'lowestPrice': requestBody['price'],
            'highestPriceLastUpdate': requestBody['timestamp'],
            'lowestPriceLastUpdate': requestBody['timestamp']
        }
        try:
            response = session.post(f'{db_hostname}/db/{url}', json=payload)
            res = response.result()
        except Exception as err:
            print('db error ... ', err)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        obj = msg.payload.decode()
        print(f"Received `{obj}` from `{msg.topic}` topic")
        json_obj = json.loads(obj)
        save_stock_db(json_obj)

    client.on_message = on_message
try:
    print('Starting MQTT Conection ...')
    time.sleep(10)
    client = cmqtt()
    subscribe(client)
    client.connect(broker, port)
    client.loop_forever()
except Exception as err:
    print('Connection MQTT Failed ...', err)