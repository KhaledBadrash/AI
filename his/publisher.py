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

def send_student_data(
    name: str,
    student_id: str,
    program: str
):
    """
    1) Peregos: name, id, program, total_credits
    2) WyseFlow: name, id, program, start_date, total_credits
    """
    details = HARD_CODED_PROGRAMS.get(program, {})
    total_credits = details.get('credits', 0)
    start_date    = details.get('start_date', '')

    base = {
        "name":          name,
        "id":            student_id,
        "program":       program,
        "total_credits": total_credits
    }

    conn    = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = conn.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    # 1) Peregos
    channel.basic_publish(
        exchange    = EXCHANGE_NAME,
        routing_key = ROUTING_KEY_PEREGOS,
        body        = json.dumps(base)
    )

    # 2) WyseFlow
    wf = dict(base, start_date=start_date)
    channel.basic_publish(
        exchange    = EXCHANGE_NAME,
        routing_key = ROUTING_KEY_WYSEFLOW,
        body        = json.dumps(wf)
    )

    conn.close()
