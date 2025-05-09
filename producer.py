from kafka import KafkaProducer
import json
import time
import random

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'weather_updates'

WEATHER_DATA = {
    "London": {"main": {"temp": 22.5}},
    "New York": {"main": {"temp": 21.3}},
    "Tokyo": {"main": {"temp": 28.7}},
    "Sydney": {"main": {"temp": 35.5}},
    "Mumbai": {"main": {"temp": 41.5}},
}

CITIES = WEATHER_DATA.keys()

def get_weather_data(city):
    if city in WEATHER_DATA:
        return {"main": {"temp": WEATHER_DATA[city]["main"]["temp"] + random.uniform(-2, 2)}}
    return None

def publish_weather_update(producer, city, temp):
    producer.send(KAFKA_TOPIC, json.dumps({'city': city, 'temperature': temp}).encode('utf-8'))
    print("Published: %s => %s" % (city, temp))

if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])

    try:
        while True:
            for city in CITIES:
                data = get_weather_data(city)
                if data and 'temp' in data['main']:
                    publish_weather_update(producer, city, data["main"]["temp"])
                time.sleep(2)
            time.sleep(10)
    except KeyboardInterrupt:
        print("Producer stopped.")
    finally:
        producer.close()
