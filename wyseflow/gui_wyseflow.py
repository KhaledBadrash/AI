import threading
import json
import pika
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_WYSEFLOW

class WyseFlowGUI:
    def __init__(self):
        # Steuer-Fenster anlegen
        self.control = tk.Tk()
        self.control.title("WyseFlow GUI")
        # „X“-Button an dieselbe Shutdown-Methode binden
        self.control.protocol("WM_DELETE_WINDOW", self._on_shutdown)

        # Log-Feld direkt im Control-Fenster
        self.log = ScrolledText(self.control, width=80, height=20, state='disabled')
        self.log.pack(fill='both', expand=True, padx=5, pady=5)

        # Shutdown-Button
        btn = tk.Button(self.control, text="Shutdown", command=self._on_shutdown)
        btn.pack(side='bottom', pady=5)

        # Nachrichtenschleife starten
        threading.Thread(target=self._consume, daemon=True).start()

    def _on_shutdown(self):
        # Fenster sofort schließen
        self.control.destroy()

    def _consume(self):
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        except pika.exceptions.AMQPConnectionError as e:
            messagebox.showerror(
                title="Connection Error",
                message=f"Could not connect to RabbitMQ:\n{e}",
                parent=self.control
            )
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

            # Feld-Checks
            if 'start_date' in msg:
                try:
                    from datetime import datetime
                    datetime.strptime(msg['start_date'], "%Y-%m-%d")
                except Exception:
                    self.control.after(0, lambda:
                        messagebox.showwarning(
                            title="Data Error",
                            message="Invalid start_date in message",
                            parent=self.control
                        )
                    )
                    continue

            # Ausgabe ins Log
            self.control.after(0, self._append, msg)

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

def main():
    # Restart-Loop
    while True:
        gui = WyseFlowGUI()
        gui.control.mainloop()

        # Nach dem Schließen erst den Dialog anzeigen
        root = tk.Tk()
        root.withdraw()
        restart = messagebox.askyesno(
            title="Restart WyseFlow?",
            message="WyseFlow GUI wurde geschlossen.\nMöchten Sie es neu starten?"
        )
        root.destroy()
        if not restart:
            break

if __name__ == "__main__":
    main()