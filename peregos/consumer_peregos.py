# peregos/consumer_peregos.py

import pika
import json
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_PEREGOS

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[PEREGOS] Empfangen: {data}")

def main():
    # Verbindung aufbauen
    conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    ch   = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    # Dynamische Queue anlegen und binden
    q = ch.queue_declare(queue='', exclusive=True).method.queue
    ch.queue_bind(exchange=EXCHANGE_NAME, queue=q, routing_key=ROUTING_KEY_PEREGOS)

    print("Peregos wartet auf Nachrichten…")
    ch.basic_consume(queue=q, on_message_callback=callback, auto_ack=True)
    ch.start_consuming()

if __name__ == '__main__':
    main()
