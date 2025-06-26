import os
import sys
import json
import re
import psutil
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

from his.publisher import send_student_data
from his.config    import HARD_CODED_PROGRAMS
from utils.validation import validate_id, validate_program

# Projekt-Root und Pfad zu students.json
PROJECT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STUDENTS_JSON = os.path.join(PROJECT_ROOT, 'students.json')

# Python-Interpreter und Environment für subprocess-Aufrufe
PY  = sys.executable
ENV = os.environ.copy()
ENV['PYTHONPATH'] = PROJECT_ROOT + os.pathsep + ENV.get('PYTHONPATH', '')

class HISGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HIS – Student Data")
        self.resizable(False, False)
        self._build_form()

    @staticmethod
    def is_module_running(module_name: str) -> bool:
        """
        Sucht in allen Prozessen nach einem CLI-Argument, das module_name enthält.
        """
        for p in psutil.process_iter(['cmdline']):
            cmd = p.info.get('cmdline') or []
            if any(module_name in arg for arg in cmd):
                return True
        return False

    def start_module(self, module_key: str):
        """
        Startet den Consumer und die GUI des Moduls, wenn es offline ist.
        """
        module_map = {
            "Peregos": [
                "peregos.consumer_peregos",
                "peregos.gui_peregos"
            ],
            "WyseFlow": [
                "wyseflow.consumer_wyseflow",
                "wyseflow.gui_wyseflow"
            ]
        }
        for module_path in module_map.get(module_key, []):
            subprocess.Popen(
                [PY, "-m", module_path],
                cwd=PROJECT_ROOT,
                env=ENV
            )

    def _build_form(self):
        # Name
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        # Student ID
        tk.Label(self, text="Student ID:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_id = tk.Entry(self, width=30)
        self.entry_id.grid(row=1, column=1, padx=5, pady=5)

        # Program
        tk.Label(self, text="Program:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cb_program = ttk.Combobox(
            self,
            values=list(HARD_CODED_PROGRAMS.keys()),
            state="readonly",
            width=28
        )
        self.cb_program.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        frame = tk.Frame(self)
        frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Send", command=self.on_send).pack(side="left", padx=5)
        tk.Button(frame, text="Exit", command=self.destroy).pack(side="right", padx=5)

    def on_send(self):
        # 1) Offline-Check & ggf. Start-Option anbieten
        offline = []
        if not self.is_module_running("peregos.consumer_peregos"):
            offline.append("Peregos")
        if not self.is_module_running("wyseflow.consumer_wyseflow"):
            offline.append("WyseFlow")

        for module in offline[:]:
            start = messagebox.askyesno(
                title="Module offline",
                message=f"{module} is offline. Do you want to start both consumer and GUI now?"
            )
            if start:
                self.start_module(module)
                offline.remove(module)

        if offline:
            messagebox.showwarning(
                "Still offline",
                f"{' and '.join(offline)} remain offline and will not receive data."
            )

        # 2) Form-Daten einlesen
        name = self.entry_name.get().strip()
        sid  = self.entry_id.get().strip()
        prog = self.cb_program.get().strip()

        # 3) Validierung
        if re.search(r"[ÄäÖöÜüß]", name):
            messagebox.showerror("Error", "Bitte ersetze Umlaute.")
            return
        if not name or not re.fullmatch(r"[A-Za-z ]+", name):
            messagebox.showerror("Error", "Name ungültig.")
            return
        if not validate_id(sid):
            messagebox.showerror("Error", "Student ID muss 7 Ziffern haben.")
            return
        if not validate_program(prog, HARD_CODED_PROGRAMS):
            messagebox.showerror("Error", f"Programm '{prog}' nicht verfügbar.")
            return

        # 4) Sendeversuch (RabbitMQ + Outbox)
        results = send_student_data(name, sid, prog)

        # 5) Immer lokal speichern
        records = []
        if os.path.isfile(STUDENTS_JSON):
            try:
                with open(STUDENTS_JSON, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            except json.JSONDecodeError:
                records = []
        records.append({"name": name, "id": sid, "program": prog})
        with open(STUDENTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2)

        # 6) Ergebnis-Meldung
        if all(results.values()):
            messagebox.showinfo("Success", "Data sent successfully to all modules.")
        else:
            failed = [k for k, ok in results.items() if not ok]
            messagebox.showwarning(
                "Partial Failure",
                f"Could not send to: {', '.join(failed)}.\n"
                "Your data has been queued and will be retried automatically."
            )

        # 7) Formular zurücksetzen
        self.reset_form()

    def reset_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.cb_program.set('')

if __name__ == "__main__":
    HISGui().mainloop()
