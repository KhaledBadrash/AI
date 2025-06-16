import json
import os
import threading
import time
import pika
from pika.exceptions import AMQPConnectionError, UnroutableError
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

def _save_outbox(msgs):
    with open(OUTBOX_PATH, 'w', encoding='utf-8') as f:
        json.dump(msgs, f, indent=2)

def _enqueue(routing_key, body):
    msgs = _load_outbox()
    msgs.append({"routing_key": routing_key, "body": body})
    _save_outbox(msgs)

def publish_with_retry(routing_key: str, body: dict) -> bool:
    """
    Versucht bis zu 3× mit exponentiellem Backoff, dann fallback-enqueue.
    Returns True on success, False if enqueued.
    """
    max_attempts = 3
    backoff = 1
    for attempt in range(1, max_attempts+1):
        try:
            conn    = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            channel = conn.channel()
            channel.confirm_delivery()
            channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
            if not channel.basic_publish(
                exchange    = EXCHANGE_NAME,
                routing_key = routing_key,
                body        = json.dumps(body)
            ):
                raise UnroutableError("unroutable")
            conn.close()
            return True
        except (AMQPConnectionError, UnroutableError):
            if attempt < max_attempts:
                time.sleep(backoff)
                backoff *= 2
                continue
            _enqueue(routing_key, body)
            return False
        except Exception:
            _enqueue(routing_key, body)
            return False

def _retry_pending():
    """
    Background: alle 40 Sekunden pending messages erneut senden.
    """
    while True:
        pending = _load_outbox()
        if pending:
            still = []
            for msg in pending:
                ok = publish_with_retry(msg['routing_key'], msg['body'])
                if not ok:
                    still.append(msg)
            if len(still) != len(pending):
                _save_outbox(still)
        time.sleep(40)   # ← hier 40 s statt 60 s

threading.Thread(target=_retry_pending, daemon=True).start()

def send_student_data(name: str, student_id: str, program: str) -> dict:
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

    return {
        'Peregos':  publish_with_retry(ROUTING_KEY_PEREGOS, base),
        'WyseFlow': publish_with_retry(ROUTING_KEY_WYSEFLOW, wf)
    }
