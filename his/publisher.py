# his/publisher.py

import json
import pika
from his.config import (
    RABBITMQ_HOST,
    EXCHANGE_NAME,
    ROUTING_KEY_PEREGOS,
    ROUTING_KEY_WYSEFLOW,
    HARD_CODED_PROGRAMS
)
from utils.validation import validate_program, validate_id

def send_student_data(name, matrikelnummer, program):
    # 1. Validierung der Eingabe
    if not name or not matrikelnummer or not program:
        raise ValueError("Alle Felder müssen ausgefüllt sein.")
    if not validate_id(matrikelnummer):
        raise ValueError("Ungültige Matrikelnummer.")
    if not validate_program(program, HARD_CODED_PROGRAMS):
        raise ValueError(f"Studiengang '{program}' nicht verfügbar.")

    # 2. Verbindung zu RabbitMQ aufbauen
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    # 3. Nachricht für Peregos (Name, ID, Programm)
    base_msg = {
        "name":    name,
        "id":      matrikelnummer,
        "program": program
    }
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY_PEREGOS,
        body=json.dumps(base_msg)
    )

    # 4. Nachricht für WyseFlow (Basis + Startdatum + Credits)
    details = HARD_CODED_PROGRAMS[program]
    wf_msg = {
        **base_msg,
        "start_date": details["start_date"],
        "credits":    details["credits"]
    }
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY_WYSEFLOW,
        body=json.dumps(wf_msg)
    )

    # 5. Verbindung schließen
    connection.close()
