"""
Terminal> python manage.py shell
Python Console> exec(open("test-script.py").read())
"""
from DataBase.models import DUser
from DataBase.models import DProject


duser = DUser()
user = duser.get_user({
    "uid": "d46ddb48e346692f861e3773d1c505fe"
})
user_dict = user.to_dict()

dproject = DProject()
project = dproject.get_project({
    "pid": "4e4d85238551a40d98b2f320fb3eb2aa"
})
project_dict = project.to_dict()
