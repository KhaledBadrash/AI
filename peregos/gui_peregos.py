import threading
import json
import time
import pika
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_PEREGOS

FIXED_RETRY_INTERVAL = 5  # Sekunden
SOCKET_TIMEOUT       = 5  # Sekunden für basic_get

class PeregosGUI:
    def __init__(self):
        self.control = tk.Tk()
        self.control.title("Peregos GUI")
        self.control.protocol("WM_DELETE_WINDOW", self.control.destroy)

        self.log = ScrolledText(self.control, width=80, height=20, state='disabled')
        self.log.pack(fill='both', expand=True, padx=5, pady=5)

        threading.Thread(target=self._consume_loop, daemon=True).start()
        self.control.mainloop()

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
                channel.queue_bind(exchange=EXCHANGE_NAME, queue=q,
                                   routing_key=ROUTING_KEY_PEREGOS)

                # Polling-Loop
                while True:
                    method, props, body = channel.basic_get(queue=q, auto_ack=True)
                    if method:
                        try:
                            msg = json.loads(body)
                        except json.JSONDecodeError:
                            # Bei kaputtem JSON Popup, dann skip
                            self.control.after(0, lambda:
                                messagebox.showwarning(
                                    "Invalid Message",
                                    f"Ungültiges JSON empfangen:\n{body!r}",
                                    parent=self.control
                                )
                            )
                            continue

                        # Append in GUI-Thread
                        self.control.after(0, lambda m=msg: self._append(m))
                    else:
                        # keine Nachricht
                        time.sleep(1)

            except pika.exceptions.AMQPConnectionError:
                # Broker down
                self.control.after(0, lambda:
                    messagebox.showwarning(
                        "Connection Lost",
                        f"Peregos disconnected. Reconnecting in {FIXED_RETRY_INTERVAL}s…",
                        parent=self.control
                    )
                )
            except Exception as e:
                # sonstige Fehler
                self.control.after(0, lambda:
                    messagebox.showwarning(
                        "Error",
                        f"Peregos consumer error: {e}\nRetrying in {FIXED_RETRY_INTERVAL}s…",
                        parent=self.control
                    )
                )
            # fixed wait before retry
            time.sleep(FIXED_RETRY_INTERVAL)

    def _append(self, msg: dict):
        lines = [
            "--- Peregos Received ---",
            f"{'Name':12s}: {msg.get('name','<missing>')}",
            f"{'Student ID':12s}: {msg.get('id','<missing>')}",
            f"{'Program':12s}: {msg.get('program','<missing>')}"
        ]
        text = "\n".join(lines) + "\n\n"
        self.log.config(state='normal')
        self.log.insert(tk.END, text)
        self.log.yview(tk.END)
        self.log.config(state='disabled')

if __name__ == "__main__":
    PeregosGUI()
