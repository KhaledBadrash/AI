import threading
import json
import pika
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from his.config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY_PEREGOS

class PeregosGUI:
    def __init__(self):
        # Steuer-Fenster
        self.control = tk.Tk()
        self.control.title("Peregos GUI")
        # Stop-Flag für den Consumer-Thread
        self._stop_event = threading.Event()
        # „X“ bindet auf dieselbe Shutdown-Logik
        self.control.protocol("WM_DELETE_WINDOW", self._on_shutdown)

        # Log-Bereich direkt im Control-Fenster
        self.log = ScrolledText(self.control, width=80, height=20, state='disabled')
        self.log.pack(fill='both', expand=True, padx=5, pady=5)

        # Shutdown-Button
        btn = tk.Button(self.control, text="Shutdown", command=self._on_shutdown)
        btn.pack(side='bottom', pady=5)

        # Consumer-Thread in den Event-Loop hinein planen,
        # damit after() legal aufgerufen werden kann:
        self.control.after(
            0,
            lambda: threading.Thread(target=self._consume, daemon=True).start()
        )

    def _on_shutdown(self):
        # 1) Consumer-Thread signalisieren, abzubrechen
        self._stop_event.set()
        # 2) RabbitMQ-Verbindung sauber schließen, falls noch offen
        try:
            if hasattr(self, 'connection') and self.connection.is_open:
                self.connection.close()
        except Exception:
            pass
        # 3) Fenster zerstören
        self.control.destroy()

    def _consume(self):
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            self.connection = conn
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
        ch.queue_bind(exchange=EXCHANGE_NAME, queue=q, routing_key=ROUTING_KEY_PEREGOS)

        # Mit inactivity_timeout, um regelmäßig das Stop-Flag prüfen zu können
        for method_frame, properties, body in ch.consume(q, auto_ack=True, inactivity_timeout=1):
            # Shutdown angefordert?
            if self._stop_event.is_set():
                break
            # Leerlauf-Timeout überspringen
            if body is None:
                continue

            try:
                msg = json.loads(body)
            except json.JSONDecodeError:
                continue

            # Beispiel-Check: total_credits > 0
            if msg.get('total_credits', 0) <= 0:
                self.control.after(0, lambda:
                    messagebox.showwarning(
                        title="Data Error",
                        message="Invalid total_credits in message",
                        parent=self.control
                    )
                )
                continue

            # Append im Try-Block, um nach destroy() sauber abbrechen zu können
            try:
                self.control.after(0, self._append, msg)
            except RuntimeError:
                break

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

def main():
    while True:
        gui = PeregosGUI()
        gui.control.mainloop()

        # erst nach Schließen den Restart-Dialog zeigen
        root = tk.Tk()
        root.withdraw()
        restart = messagebox.askyesno(
            title="Restart Peregos?",
            message="Peregos GUI wurde geschlossen.\nMöchten Sie es neu starten?"
        )
        root.destroy()
        if not restart:
            break

if __name__ == "__main__":
    main()
