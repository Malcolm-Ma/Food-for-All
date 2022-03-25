from DataBase.models import *
from Common.common import *
from Login.functions import *

def get_user_decorator(force_login=True):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            user = check_login(request)
            if not user and force_login:
                response_data = {"status": ""}
                response_data["status"] = STATUS_CODE["user_not_logged_in"]
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            kwargs["user"] = user
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator