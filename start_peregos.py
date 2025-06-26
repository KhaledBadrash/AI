#!/usr/bin/env python3
import os
import subprocess
import sys

# 1) Projekt-Root ermitteln
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 2) PYTHONPATH sicherstellen
env = os.environ.copy()
env['PYTHONPATH'] = PROJECT_ROOT + os.pathsep + env.get('PYTHONPATH', '')

# 3) Python-Interpreter anzeigen
PY = sys.executable
print("Using Python:", PY)
print("Project root:", PROJECT_ROOT)
print("PYTHONPATH:", env['PYTHONPATH'])

# 4) Befehle vorbereiten
consumer_cmd = [PY, "-m", "peregos.consumer_peregos"]
gui_cmd      = [PY, "-m", "peregos.gui_peregos"]

# 5) Consumer starten
print("Starting Peregos consumer:", consumer_cmd)
try:
    p1 = subprocess.Popen(consumer_cmd, cwd=PROJECT_ROOT, env=env)
    print("Consumer PID:", p1.pid)
except Exception as e:
    print("Failed to start consumer:", e)

# 6) GUI starten
print("Starting Peregos GUI:", gui_cmd)
try:
    p2 = subprocess.Popen(gui_cmd, cwd=PROJECT_ROOT, env=env)
    print("GUI PID:", p2.pid)
except Exception as e:
    print("Failed to start GUI:", e)

# 7) Auf Prozesse warten und Exit-Codes ausgeben
if 'p1' in locals():
    ret1 = p1.wait()
    print("Consumer exited with code", ret1)
if 'p2' in locals():
    ret2 = p2.wait()
    print("GUI exited with code", ret2)
