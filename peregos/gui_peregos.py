# peregos/gui_peregos.py

import threading
import json
import pika
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_PEREGOS

class PeregosGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Peregos – Nachrichten")
        self.log = ScrolledText(self.root, width=80, height=20, state='disabled')
        self.log.pack(padx=10, pady=10, fill='both', expand=True)

        # Startet die RabbitMQ-Consumer-Schleife in einem Hintergrund-Thread
        t = threading.Thread(target=self.consume, daemon=True)
        t.start()

        self.root.mainloop()

    def consume(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel    = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

        q = channel.queue_declare(queue='', exclusive=True).method.queue
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=q, routing_key=ROUTING_KEY_PEREGOS)

        for method, properties, body in channel.consume(q, auto_ack=True):
            msg = json.loads(body)
            self.log_message(msg)

    def log_message(self, msg: dict):
        # Muss im Hauptthread passieren, darum root.after
        def append():
            self.log.config(state='normal')
            self.log.insert(tk.END, f"{msg}\n")
            self.log.yview(tk.END)
            self.log.config(state='disabled')
        self.root.after(0, append)

if __name__ == "__main__":
    PeregosGUI()
