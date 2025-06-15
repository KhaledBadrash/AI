# start_all.py

import threading
import subprocess
import sys

PYTHON = sys.executable

modules = [
    "peregos.gui_peregos",
    "wyseflow.gui_wyseflow",
    "his.his_gui"
]

threads = []
for mod in modules:
    cmd = [PYTHON, "-m", mod]
    t = threading.Thread(target=subprocess.run, args=(cmd,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
