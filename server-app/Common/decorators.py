import time

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
                        response_data = {"status": STATUS_CODE["invalid request parameters"]}
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
                #response_data["status"] = STATUS_CODE["project does not exist"]
                #return HttpResponse(json.dumps(response_data), content_type="application/json")
                raise ServerError("project does not exist")
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
                #response_data["status"] = STATUS_CODE["user has not logged in"]
                #return HttpResponse(json.dumps(response_data), content_type="application/json")
                raise ServerError("user has not logged in")
            kwargs["user"] = user
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator

def record_login_fail_decorator():
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
            except ServerError as se:
                request = args[0]
                cache_attempts = caches[MAX_FAILED_LOGIN_ATTEMPTS_KEY]
                url = get_request_url(request)
                login_attempts = [] if not cache_attempts.get(url) else cache_attempts.get(url)
                login_attempts = [i for i in login_attempts if i > int(time.time()) - MAX_FAILED_LOGIN_INTERVAL_ALLOWED]
                login_attempts.append(int(time.time()))
                cache_attempts.set(url, login_attempts, timeout=MAX_FAILED_LOGIN_INTERVAL_ALLOWED)
                if len(login_attempts) >= MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED:
                    cache_forbidden = caches[LOGIN_FORBIDDEN_KEY]
                    cache_forbidden.set(url, True, timeout=MAX_FAILED_LOGIN_INTERVAL_ALLOWED)
                response = se.response()
            return response
        return wrapped_function
    return decorator

def check_login_forbidden_decorator():
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            url = get_request_url(request)
            cache_forbidden = caches[LOGIN_FORBIDDEN_KEY]
            if cache_forbidden.get(url):
                response_data = {"status": STATUS_CODE["temporary ban due to too frequent login attempts"]}
                return HttpResponseBadRequest(json.dumps(response_data), content_type="application/json")
            else:
                return func(*args, **kwargs)
        return wrapped_function
    return decorator