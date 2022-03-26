from Login.functions import check_login
from Common.common import *
from DataBase.models import *

def api_logger_decorator(logger=logger_standard):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            response = func(*args, **kwargs)
            try:
                request_data = request.body.decode()
            except:
                request_data = ""
            logger.info("[{uid}] - [Request] [{url}] [{method}] [{path_info}] [{request_data}] - [Response] [{status_code}] [{response_data}]".format(url=get_request_url(request), method=request.method, path_info=request.path_info, request_data=request_data, status_code=str(response.status_code), response_data=response.content.decode(), uid="guest" if not check_login(request) else check_login(request).uid))
            return response
        return wrapped_function
    return decorator

def check_request_method_decorator(method=("POST",)):
    if type(method) == str:
        method = [method]
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            if request.method not in method:
                return HttpResponseNotAllowed(method)
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator

def check_request_parameters_decorator(params=()):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if params:
                request = args[0]
                data = json.loads(request.body)
                for i in params:
                    if i not in data:
                        response_data = {"status": STATUS_CODE["request_parameters_wrong"]}
                        return HttpResponseBadRequest(json.dumps(response_data), content_type="application/json")
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator

def check_server_error_decorator():
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
            except ServerError as se:
                response = se.response()
            return response
        return wrapped_function
    return decorator

def get_project_decorator(force_exist=True):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            data = json.loads(request.body)
            pid = data["pid"]
            project = DProject.get_project({"pid": pid})
            if not project and force_exist:
                #response_data = {"status": ""}
                #response_data["status"] = STATUS_CODE["project_not_exists"]
                #return HttpResponse(json.dumps(response_data), content_type="application/json")
                raise ServerError("project_not_exists")
            kwargs["project"] = project
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator

def get_user_decorator(force_login=True):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            user = check_login(request)
            if not user and force_login:
                #response_data = {"status": ""}
                #response_data["status"] = STATUS_CODE["user_not_logged_in"]
                #return HttpResponse(json.dumps(response_data), content_type="application/json")
                raise ServerError("user_not_logged_in")
            kwargs["user"] = user
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator