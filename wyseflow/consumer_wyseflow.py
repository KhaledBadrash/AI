import threading
import json
import time
import pika
import tkinter as tk
from tkinter import messagebox
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_WYSEFLOW

FIXED_RETRY_INTERVAL = 5  # Sekunden zwischen Reconnect-Versuchen
SOCKET_TIMEOUT       = 5  # s für jeden basic_get-Aufruf

class WyseFlowConsumer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        threading.Thread(target=self._consume_loop, daemon=True).start()

    def _consume_loop(self):
        while True:
            try:
                params = pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    heartbeat=0,
                    socket_timeout=SOCKET_TIMEOUT
                )
                conn    = pika.BlockingConnection(params)
                channel = conn.channel()
                channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

                q = channel.queue_declare(queue='', exclusive=True).method.queue
                channel.queue_bind(exchange=EXCHANGE_NAME, queue=q, routing_key=ROUTING_KEY_WYSEFLOW)

                while True:
                    try:
                        method, props, body = channel.basic_get(queue=q, auto_ack=True)
                    except Exception:
                        raise

                    if method:
                        msg = json.loads(body)
                        # Datum‐Check
                        if 'start_date' in msg:
                            try:
                                from datetime import datetime
                                datetime.strptime(msg['start_date'], "%Y-%m-%d")
                            except:
                                self.root.after(0, lambda:
                                    messagebox.showwarning(
                                        "Data Error",
                                        "Invalid start_date in message",
                                        parent=self.root
                                    )
                                )
                                continue
                        print("[WYSEFLOW]", msg)
                    else:
                        time.sleep(1)

            except pika.exceptions.AMQPConnectionError:
                self.root.after(0, lambda:
                    messagebox.showwarning(
                        "Connection Lost",
                        f"WyseFlow disconnected. Reconnecting in {FIXED_RETRY_INTERVAL}s…",
                        parent=self.root
                    )
                )
            except Exception as e:
                self.root.after(0, lambda:
                    messagebox.showwarning(
                        "Consumer Error",
                        f"WyseFlow consumer error: {e}\nRetrying in {FIXED_RETRY_INTERVAL}s…",
                        parent=self.root
                    )
                )

            time.sleep(FIXED_RETRY_INTERVAL)

def main():
    WyseFlowConsumer()
    tk.mainloop()

if __name__ == "__main__":
    main()
