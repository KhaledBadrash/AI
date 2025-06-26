#!/usr/bin/env python3
import subprocess, sys

PY = sys.executable
# nur das HIS-GUI
subprocess.Popen([PY, "-m", "his.his_gui"])
