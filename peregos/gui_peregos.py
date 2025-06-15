# peregos/gui_peregos.py

import threading, json, pika, tkinter as tk
from tkinter.scrolledtext import ScrolledText
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_PEREGOS

class PeregosGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Peregos – Messages")
        self.log  = ScrolledText(self.root, state='disabled', width=80, height=20)
        self.log.pack(fill='both', expand=True, padx=5, pady=5)

        t = threading.Thread(target=self.consume, daemon=True)
        t.start()
        self.root.mainloop()

    def consume(self):
        conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        ch   = conn.channel()
        ch.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
        q    = ch.queue_declare(queue='', exclusive=True).method.queue
        ch.queue_bind(exchange=EXCHANGE_NAME, queue=q, routing_key=ROUTING_KEY_PEREGOS)

        for _, _, body in ch.consume(q, auto_ack=True):
            msg = json.loads(body)
            self.root.after(0, self._append, msg)

    def _append(self, msg):
        self.log.config(state='normal')
        self.log.insert(tk.END, f"{msg}\n")
        self.log.yview(tk.END)
        self.log.config(state='disabled')

if __name__ == "__main__":
    PeregosGUI()
