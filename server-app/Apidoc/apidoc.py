import os
import subprocess
from pathlib import Path
import platform

CURRENT_DIR = Path(__file__).resolve().parent

isShell = platform.system() == 'Windows'

p = subprocess.Popen(['npm', 'run', 'doc'], shell=isShell, cwd=CURRENT_DIR, stderr=subprocess.PIPE)
p.wait()  # wait for response
npm_res = p.returncode

if npm_res == 0:
    print("Generating API doc ...")
else:
    print("No apidoc detected, installing ...")
    os.chdir('Apidoc')
    os.system("npm install")
    os.system('npm run doc')
    os.chdir('..')
