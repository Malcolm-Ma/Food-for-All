import os
import subprocess
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

# if __name__ != "__main__":
#     from FoodForAll.settings import DOC_DIR
# else:
#     DOC_PATH = "./DOC/"
#
# api_path = ["Common", "Login", "Payment", "Project", "Upload", "User"]
# command = "apidoc"
# output_path = os.path.join(DOC_DIR, "apidoc")
# config_file = os.path.join(Path(__file__).resolve().parent, "apidoc.json")
#
# for i in api_path:
#     command += " -i \"{path}\"".format(path=i)
# command += " -o \"{path}\"".format(path=output_path)
# command += " -c \"{path}\"".format(path=config_file)

# os.system(command)

p = subprocess.Popen(['npm', 'run', 'doc'], shell=True, cwd=CURRENT_DIR, stderr=subprocess.PIPE)
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
