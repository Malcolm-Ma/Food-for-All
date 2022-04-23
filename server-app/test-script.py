"""
PyCharm Terminal      > python manage.py shell
(Interactive Console) > exec(open("test-script.py").read())
"""
from Statistics.functions import Statistics


pid = "4e4d85238551a40d98b2f320fb3eb2aa"
uid1 = "d46ddb48e346692f861e3773d1c505fe"  # type == 1 (charity)
uid2 = "a964964d43975d779d774ce866b371d4"  # type == 2 (guest)

Statistics.generate_report(pid)
