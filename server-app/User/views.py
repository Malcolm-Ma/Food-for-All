from Login.functions import check_login
import json
from django.http import HttpResponse

def get_user_info(request):
    response_data = {"uid": "",
                     "mail": "",
                     "name": "",
                     "avatar": "",
                     "type": "",
                     "region": "",
                     "currency_type": "GBP",
                     "project": "",
                     "regis_time": 0,
                     "last_login_time": 0,
                     "donate_history": "",
                     "share_mail_history": ""}
    user_info = check_login(request)
    if user_info:
        for i in response_data:
            response_data[i] = user_info.__getattribute__(i)
    return HttpResponse(json.dumps(response_data), content_type="application/json")