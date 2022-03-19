import os
if __name__ != "__main__":
    from FoodForAll.settings import DOC_PATH
else:
    DOC_PATH = "./DOC/"
from pathlib import Path

api_path = ["Common", "Login", "Payment", "Project", "Upload", "User"]
command = "apidoc"
output_path = os.path.join(DOC_PATH, "apidoc")
config_file = os.path.join(Path(__file__).resolve().parent, "apidoc.json")

for i in api_path:
    command += " -i {path}".format(path=i)
command += " -o {path}".format(path=output_path)
command += " -c {path}".format(path=config_file)

os.system(command)