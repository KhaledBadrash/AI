# his/his_gui.py

import tkinter as tk
from tkinter import messagebox, ttk
from publisher import send_student_data
from config import HARD_CODED_PROGRAMS
from utils.validation import validate_id, validate_program

class HISGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HIS – Studierendendaten")
        self.resizable(False, False)

        # -- Labels und Felder --
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=8, pady=4, sticky="e")
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(self, text="Matrikelnummer:").grid(row=1, column=0, padx=8, pady=4, sticky="e")
        self.entry_id = tk.Entry(self, width=30)
        self.entry_id.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(self, text="Studiengang:").grid(row=2, column=0, padx=8, pady=4, sticky="e")
        # Combobox mit readonly, damit nur Auswahl möglich ist
        self.cb_program = ttk.Combobox(
            self,
            values=list(HARD_CODED_PROGRAMS.keys()),
            state="readonly",
            width=28
        )
        self.cb_program.grid(row=2, column=1, padx=8, pady=4)
        # Bei Fokus öffnet sich automatisch das Dropdown
        self.cb_program.bind(
            "<FocusIn>",
            lambda e: self.cb_program.event_generate("<Down>")
        )

        # -- Senden Button --
        btn_send = tk.Button(self, text="Senden", command=self.on_submit)
        btn_send.grid(row=3, column=0, columnspan=2, pady=10)

    def on_submit(self):
        name       = self.entry_name.get().strip()
        student_id = self.entry_id.get().strip()
        program    = self.cb_program.get().strip()

        # -- Validierung --
        if not name:
            messagebox.showerror("Fehler", "Bitte Namen eingeben.")
            return
        if not validate_id(student_id):
            messagebox.showerror("Fehler", "Ungültige Matrikelnummer.")
            return
        if not validate_program(program):
            messagebox.showerror("Fehler", f"Studiengang „{program}“ nicht verfügbar.")
            return

        # -- Daten senden --
        try:
            send_student_data(name, student_id, program)
            messagebox.showinfo("Erfolg", "Daten erfolgreich gesendet.")
            # Formular zurücksetzen
            self.entry_name.delete(0, tk.END)
            self.entry_id.delete(0, tk.END)
            self.cb_program.set('')
        except Exception as exc:
            messagebox.showerror("Fehler", f"Fehler beim Versenden:\n{exc}")

if __name__ == "__main__":
    app = HISGui()
    app.mainloop()
