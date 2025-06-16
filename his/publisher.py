# his/publisher.py

import json
import os
import threading
import time
import pika
from his.config import (
    RABBITMQ_HOST,
    EXCHANGE_NAME,
    ROUTING_KEY_PEREGOS,
    ROUTING_KEY_WYSEFLOW,
    HARD_CODED_PROGRAMS
)

OUTBOX_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'outbox.json')
)

def _load_outbox():
    if not os.path.isfile(OUTBOX_PATH):
        return []
    try:
        with open(OUTBOX_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_outbox(messages):
    with open(OUTBOX_PATH, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2)

def _enqueue(routing_key, body):
    messages = _load_outbox()
    messages.append({"routing_key": routing_key, "body": body})
    _save_outbox(messages)

def publish_message(routing_key: str, body: dict) -> bool:
    """
    Versucht, eine Nachricht zu publishen.
    Gibt True zurück, wenn sofort gesendet, False wenn in Outbox gequeued.
    """
    try:
        conn    = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = conn.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
        channel.basic_publish(
            exchange    = EXCHANGE_NAME,
            routing_key = routing_key,
            body        = json.dumps(body)
        )
        conn.close()
        return True
    except Exception:
        _enqueue(routing_key, body)
        return False

def _retry_pending():
    while True:
        pending = _load_outbox()
        if pending:
            still = []
            for msg in pending:
                ok = publish_message(msg['routing_key'], msg['body'])
                if not ok:
                    still.append(msg)
            if len(still) != len(pending):
                _save_outbox(still)
        time.sleep(60)

threading.Thread(target=_retry_pending, daemon=True).start()

def send_student_data(name: str, student_id: str, program: str) -> dict:
    """
    Schickt Daten an Peregos und WyseFlow.
    Returns: {"Peregos": bool, "WyseFlow": bool}
    """
    details       = HARD_CODED_PROGRAMS.get(program, {})
    total_credits = details.get('credits', 0)
    start_date    = details.get('start_date', '')

    base = {
        "name":          name,
        "id":            student_id,
        "program":       program,
        "total_credits": total_credits
    }
    wf = dict(base, start_date=start_date)

    results = {}
    results['Peregos']  = publish_message(ROUTING_KEY_PEREGOS, base)
    results['WyseFlow'] = publish_message(ROUTING_KEY_WYSEFLOW, wf)
    return results
