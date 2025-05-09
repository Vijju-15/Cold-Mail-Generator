# coding=utf-8
from kafka import KafkaConsumer
import json

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'weather_updates'

def process_weather_update(msg):
    try:
        data = json.loads(msg.value)
        city = data['city']
        temp = data['temperature']
        if temp >= 40:
            print("ALERT: %s - %.1f°C" % (city, temp))
        else:
            print("OK: %s - %.1f°C" % (city, temp))
    except Exception as e:
        print("Error processing: %s - %s" % (msg.value, e))

if __name__ == "__main__":
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='weather_consumer_group'
    )
    print("Consumer started...")
    try:
        for msg in consumer:
            process_weather_update(msg)
    except KeyboardInterrupt:
        print("Consumer stopped.")
    finally:
        consumer.close()
