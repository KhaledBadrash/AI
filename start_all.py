# start_all.py

import threading
import subprocess

services = [
    ["python", "peregos/consumer_peregos.py"],
    ["python", "wyseflow/consumer_wyseflow.py"],
    ["python", "his/his_gui.py"]
]

threads = []
for cmd in services:
    t = threading.Thread(target=subprocess.run, args=(cmd,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
