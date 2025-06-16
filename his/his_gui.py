# his/his_gui.py

import os
import json
import re
import tkinter as tk
from tkinter import messagebox, ttk

from his.publisher import send_student_data
from his.config    import HARD_CODED_PROGRAMS
from utils.validation import validate_id, validate_program

# Projekt-Wurzel, um students.json zu finden
PROJECT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STUDENTS_JSON = os.path.join(PROJECT_ROOT, 'students.json')

class HISGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HIS – Student Data")
        self.resizable(False, False)
        self._build_form()

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
        name = self.entry_name.get().strip()
        sid  = self.entry_id.get().strip()
        prog = self.cb_program.get().strip()

        # Validierung
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

        # Sendeversuch (RabbitMQ + Outbox)
        send_student_data(name, sid, prog)

        # Immer lokal speichern
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

        # Erfolgsmeldung
        messagebox.showinfo("Success", "Data sent successfully.")

        self.reset_form()

    def reset_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.cb_program.set('')

if __name__ == "__main__":
    HISGui().mainloop()
