import threading
import json
import time
import pika
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_WYSEFLOW

FIXED_RETRY_INTERVAL = 5  # Sekunden
SOCKET_TIMEOUT       = 5  # Sekunden für basic_get

class WyseFlowGUI:
    def __init__(self):
        self.control = tk.Tk()
        self.control.title("WyseFlow GUI")
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
                                   routing_key=ROUTING_KEY_WYSEFLOW)

                while True:
                    method, props, body = channel.basic_get(queue=q, auto_ack=True)
                    if method:
                        try:
                            msg = json.loads(body)
                        except json.JSONDecodeError:
                            self.control.after(0, lambda:
                                messagebox.showwarning(
                                    "Invalid Message",
                                    f"Ungültiges JSON empfangen:\n{body!r}",
                                    parent=self.control
                                )
                            )
                            continue

                        # Datum prüfen
                        if 'start_date' in msg:
                            try:
                                from datetime import datetime
                                datetime.strptime(msg['start_date'], "%Y-%m-%d")
                            except:
                                self.control.after(0, lambda:
                                    messagebox.showwarning(
                                        "Data Error",
                                        "Invalid start_date in message",
                                        parent=self.control
                                    )
                                )
                                continue

                        self.control.after(0, lambda m=msg: self._append(m))
                    else:
                        time.sleep(1)

            except pika.exceptions.AMQPConnectionError:
                self.control.after(0, lambda:
                    messagebox.showwarning(
                        "Connection Lost",
                        f"WyseFlow disconnected. Reconnecting in {FIXED_RETRY_INTERVAL}s…",
                        parent=self.control
                    )
                )
            except Exception as e:
                self.control.after(0, lambda:
                    messagebox.showwarning(
                        "Error",
                        f"WyseFlow consumer error: {e}\nRetrying in {FIXED_RETRY_INTERVAL}s…",
                        parent=self.control
                    )
                )
            time.sleep(FIXED_RETRY_INTERVAL)

    def _append(self, msg: dict):
        lines = [
            "--- WyseFlow Received ---",
            f"{'Name':12s}: {msg.get('name','<missing>')}",
            f"{'Student ID':12s}: {msg.get('id','<missing>')}",
            f"{'Program':12s}: {msg.get('program','<missing>')}"
        ]
        if 'start_date' in msg:
            lines.append(f"{'Start Date':12s}: {msg['start_date']}")
        if 'total_credits' in msg:
            lines.append(f"{'Total Credits':12s}: {msg['total_credits']}")

        text = "\n".join(lines) + "\n\n"
        self.log.config(state='normal')
        self.log.insert(tk.END, text)
        self.log.yview(tk.END)
        self.log.config(state='disabled')

if __name__ == "__main__":
    WyseFlowGUI()
