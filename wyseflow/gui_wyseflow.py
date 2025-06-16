import threading
import json
import pika
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_WYSEFLOW

class WyseFlowGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WyseFlow – Messages")
        self.log  = ScrolledText(self.root, width=80, height=20, state='disabled')
        self.log.pack(fill='both', expand=True, padx=5, pady=5)

        threading.Thread(target=self.consume, daemon=True).start()
        self.root.mainloop()

    def consume(self):
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        except pika.exceptions.AMQPConnectionError as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Connection Error", f"Could not connect to RabbitMQ:\n{e}"
            ))
            return

        ch = conn.channel()
        ch.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

        q = ch.queue_declare(queue='', exclusive=True).method.queue
        ch.queue_bind(exchange=EXCHANGE_NAME, queue=q, routing_key=ROUTING_KEY_WYSEFLOW)

        for _, _, body in ch.consume(q, auto_ack=True):
            try:
                msg = json.loads(body)
            except json.JSONDecodeError:
                continue

            self.root.after(0, self._append, msg)

    def _append(self, msg: dict):
        try:
            lines = ["--- WyseFlow Received ---"]
            lines.append(f"{'Name':12s}: {msg['name']}")
            lines.append(f"{'Student ID':12s}: {msg['id']}")
            lines.append(f"{'Program':12s}: {msg['program']}")
            if 'start_date' in msg:
                lines.append(f"{'Start Date':12s}: {msg['start_date']}")
            if 'total_credits' in msg:
                lines.append(f"{'Total Credits':12s}: {msg['total_credits']}")
            text = "\n".join(lines) + "\n\n"
        except KeyError as e:
            messagebox.showwarning(
                "Data Error", f"Missing expected field: {e}"
            )
            return

        self.log.config(state="normal")
        self.log.insert(tk.END, text)
        self.log.yview(tk.END)
        self.log.config(state="disabled")

if __name__ == "__main__":
    WyseFlowGUI()
