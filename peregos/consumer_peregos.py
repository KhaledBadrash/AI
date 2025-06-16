import threading
import json
import time
import pika
import tkinter as tk
from tkinter import messagebox
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_PEREGOS

FIXED_RETRY_INTERVAL = 5  # Sekunden zwischen Reconnect-Versuchen
SOCKET_TIMEOUT       = 5  # s für jeden basic_get-Aufruf

class PeregosConsumer:
    def __init__(self):
        # Unsichtbare Tk-Root nur für Popups
        self.root = tk.Tk()
        self.root.withdraw()
        threading.Thread(target=self._consume_loop, daemon=True).start()

    def _consume_loop(self):
        while True:
            try:
                # Verbindung mit kurzem Socket-Timeout aufbauen
                params = pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    heartbeat=0,
                    socket_timeout=SOCKET_TIMEOUT
                )
                conn    = pika.BlockingConnection(params)
                channel = conn.channel()
                channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

                # anonyme Queue und binden
                q = channel.queue_declare(queue='', exclusive=True).method.queue
                channel.queue_bind(exchange=EXCHANGE_NAME, queue=q, routing_key=ROUTING_KEY_PEREGOS)

                # Polling-Schleife
                while True:
                    try:
                        method, props, body = channel.basic_get(queue=q, auto_ack=True)
                    except Exception:
                        # Sobald basic_get fehlschlägt, werfen wir zur reconnect-Logik
                        raise

                    if method:
                        # erfolgreiche Nachricht
                        msg = json.loads(body)
                        print("[PEREGOS]", msg)
                    else:
                        # keine Nachricht, kurz warten
                        time.sleep(1)

            except pika.exceptions.AMQPConnectionError:
                self.root.after(0, lambda:
                    messagebox.showwarning(
                        "Connection Lost",
                        f"Peregos disconnected. Reconnecting in {FIXED_RETRY_INTERVAL}s…",
                        parent=self.root
                    )
                )
            except Exception as e:
                self.root.after(0, lambda:
                    messagebox.showwarning(
                        "Consumer Error",
                        f"Peregos consumer error: {e}\nRetrying in {FIXED_RETRY_INTERVAL}s…",
                        parent=self.root
                    )
                )

            # auf jeden Fall warten und dann neu verbinden
            time.sleep(FIXED_RETRY_INTERVAL)

def main():
    PeregosConsumer()
    tk.mainloop()

if __name__ == "__main__":
    main()
