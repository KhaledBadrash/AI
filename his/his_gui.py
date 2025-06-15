# his/his_gui.py

import os
import json
import tkinter as tk
from tkinter import messagebox, ttk
from his.publisher import send_student_data
from his.config import HARD_CODED_PROGRAMS
from utils.validation import validate_id, validate_program, validate_modules

STUDENTS_JSON = os.path.join(os.path.dirname(__file__), '..', 'students.json')

class HISGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HIS – Student Data")
        self.resizable(False, False)

        # Name
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        # Student ID
        tk.Label(self, text="Student ID:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_id = tk.Entry(self, width=30)
        self.entry_id.grid(row=1, column=1, padx=5, pady=5)

        # Program Combobox
        tk.Label(self, text="Program:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cb_program = ttk.Combobox(
            self, values=list(HARD_CODED_PROGRAMS.keys()),
            state="readonly", width=28
        )
        self.cb_program.grid(row=2, column=1, padx=5, pady=5)
        self.cb_program.bind("<<ComboboxSelected>>", self.on_program_selected)

        # Modules Listbox (optional)
        tk.Label(self, text="Modules (optional):").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        self.lb_modules = tk.Listbox(self, selectmode="multiple", width=30, height=10, exportselection=False)
        self.lb_modules.grid(row=3, column=1, padx=5, pady=5)
        self.lb_modules.configure(state="disabled")

        # Send Button
        tk.Button(self, text="Send", command=self.on_send).grid(row=4, column=0, columnspan=2, pady=10)

    def on_program_selected(self, _):
        """Populate modules when a program is chosen."""
        prog = self.cb_program.get()
        self.lb_modules.delete(0, tk.END)
        for m in HARD_CODED_PROGRAMS[prog]['modules']:
            self.lb_modules.insert(tk.END, m['name'])
        self.lb_modules.configure(state="normal")

    def on_send(self):
        name    = self.entry_name.get().strip()
        sid     = self.entry_id.get().strip()
        prog    = self.cb_program.get().strip()
        modules = [self.lb_modules.get(i) for i in self.lb_modules.curselection()]

        # Validations
        if not name:
            messagebox.showerror("Error", "Please enter a name."); return
        if not validate_id(sid):
            messagebox.showerror("Error", "Invalid student ID."); return
        if not validate_program(prog, HARD_CODED_PROGRAMS):
            messagebox.showerror("Error", f"Program '{prog}' unavailable."); return
        if modules and not validate_modules(prog, modules, HARD_CODED_PROGRAMS):
            messagebox.showerror("Error", "One or more modules invalid."); return

        # Publish & save locally
        try:
            send_student_data(name, sid, prog, modules)
            self.append_to_json({
                "name": name,
                "id": sid,
                "program": prog,
                "modules": modules,
                "start_date": HARD_CODED_PROGRAMS[prog]['start_date'],
                "total_credits": HARD_CODED_PROGRAMS[prog]['credits']
            })
            messagebox.showinfo("Success", "Data sent successfully.")
            self.reset_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send data:\n{e}")

    def append_to_json(self, record: dict):
        """Append the record to students.json (create if missing)."""
        path = os.path.abspath(STUDENTS_JSON)
        data = []
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []
        data.append(record)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def reset_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.cb_program.set('')
        self.lb_modules.delete(0, tk.END)
        self.lb_modules.configure(state="disabled")

if __name__ == "__main__":
    HISGui().mainloop()
