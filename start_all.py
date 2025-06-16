# start_all.py

import threading
import subprocess
import sys

PY = sys.executable
MODULES = [
    "peregos.consumer_peregos",
    "peregos.gui_peregos",
    "wyseflow.consumer_wyseflow",
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
#Set-ExecutionPolicy RemoteSigned -Scope Process -Force
#>> .\.venv\Scripts\Activate.ps1

#
#Set-ExecutionPolicy RemoteSigned -Scope Process -Force
#>> .\.venv\Scripts\Activate.ps1

#