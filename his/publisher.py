# his/publisher.py

import json
import pika
from his.config import (
    RABBITMQ_HOST, EXCHANGE_NAME,
    ROUTING_KEY_PEREGOS, ROUTING_KEY_WYSEFLOW
)

def send_student_data(name: str, student_id: str,
                      program: str, modules: list):
    """
    Publish two messages:
      1) to Peregos: name, id, program, modules
      2) to WyseFlow: includes start_date & total_credits
    """
    conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    ch   = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    base = {
        "name": name,
        "id":   student_id,
        "program": program,
        "modules": modules
    }

    # Peregos
    ch.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY_PEREGOS,
        body=json.dumps(base)
    )

    # WyseFlow
    from his.config import HARD_CODED_PROGRAMS
    details = HARD_CODED_PROGRAMS[program]
    wf = dict(base)
    wf["start_date"]    = details["start_date"]
    wf["total_credits"] = details["credits"]

    ch.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY_WYSEFLOW,
        body=json.dumps(wf)
    )

    conn.close()
