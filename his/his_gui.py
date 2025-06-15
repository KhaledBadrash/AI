# his/his_gui.py

import tkinter as tk
from tkinter import messagebox
from publisher import send_student_data

def on_submit():
    try:
        send_student_data(
            entry_name.get().strip(),
            entry_id.get().strip(),
            entry_program.get().strip()
        )
        messagebox.showinfo("Erfolg", "Daten erfolgreich gesendet.")
        entry_name.delete(0, tk.END)
        entry_id.delete(0, tk.END)
        entry_program.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

# Fenster initialisieren
root = tk.Tk()
root.title("HIS – Studierendendaten")

# Eingabefelder
tk.Label(root, text="Name:").grid(row=0, column=0, pady=4, sticky='e')
entry_name    = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Matrikelnummer:").grid(row=1, column=0, pady=4, sticky='e')
entry_id      = tk.Entry(root, width=30)
entry_id.grid(row=1, column=1)

tk.Label(root, text="Studiengang:").grid(row=2, column=0, pady=4, sticky='e')
entry_program = tk.Entry(root, width=30)
entry_program.grid(row=2, column=1)

# Senden-Button
tk.Button(root, text="Senden", command=on_submit)\
    .grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
