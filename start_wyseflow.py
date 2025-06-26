#!/usr/bin/env python3
import os
import subprocess
import sys

# Projekt-Root ermitteln
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Sicherstellen, dass unser Projekt im PYTHONPATH ist
env = os.environ.copy()
env['PYTHONPATH'] = PROJECT_ROOT + os.pathsep + env.get('PYTHONPATH', '')

PY = sys.executable

# Prozesse starten
processes = [
    subprocess.Popen(
        [PY, "-m", "wyseflow.consumer_wyseflow"],
        cwd=PROJECT_ROOT,
        env=env
    ),
    subprocess.Popen(
        [PY, "-m", "wyseflow.gui_wyseflow"],
        cwd=PROJECT_ROOT,
        env=env
    )
]

# Warten, bis beide Fenster geschlossen werden
for p in processes:
    p.wait()
