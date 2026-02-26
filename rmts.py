import subprocess
import os
import sys

# 1. Create the virtual environment
venv_dir = ".zenv"
subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

# 2. Define the path to the venv's Python executable
# On Windows, it's in 'Scripts'; on macOS/Linux, it's in 'bin'
if os.name == "nt":
    venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
else:
    venv_python = os.path.join(venv_dir, "bin", "python")

# 3. Use the venv's Python directly to install requirements
# This ensures pip installs into the .zenv folder, not globally
subprocess.run([venv_python, "-m", "pip", "install", "-r", "rmts.txt"], check=True)
