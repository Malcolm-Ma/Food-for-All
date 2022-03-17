import os

api_path = ["Common", "Login", "Payment", "Project", "Upload", "User"]
command = "apidoc"
output_path = "Apidoc"
config_file = os.path.join(output_path, "apidoc.json")

for i in api_path:
    command += " -i {path}".format(path=i)
command += " -o {path}".format(path=output_path)
command += " -c {path}".format(path=config_file)

os.system(command)