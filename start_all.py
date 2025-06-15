# start_all.py

import threading, subprocess, sys

PY = sys.executable
MODULES = [
    "peregos.gui_peregos",
    "wyseflow.gui_wyseflow",
    "his.his_gui"
]

threads = []
for m in MODULES:
    cmd = [PY, "-m", m]
    t = threading.Thread(target=subprocess.run, args=(cmd,), daemon=True)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
