from Login.functions import check_login
from Common.common import *
from DataBase.models import *

# This document defines a number of generic interface function decorators

# Decorator for log output
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
            # Print log
            logger.info("[{uid}] - [Request] [{url}] [{method}] [{path_info}] [{request_data}] - [Response] [{status_code}] [{response_data}]".format(url=get_request_url(request), method=request.method, path_info=request.path_info, request_data=request_data, status_code=str(response.status_code), response_data=response.content.decode(), uid="guest" if not check_login(request) else check_login(request).uid))
            return response
        return wrapped_function
    return decorator

# Decorator for validating request method
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

# Decorator for verifying whether request parameters are reasonable
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

# Decorator to validate error status codes and convert to readable output
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

# Decorator to get project information from the request content
def get_project_decorator(force_exist=True):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            data = json.loads(request.body)
            pid = data["pid"]
            project = DProject.get_project({"pid": pid})
            if not project and force_exist:
                raise ServerError("project does not exist")
            kwargs["project"] = project
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator

# Decorator to get user information from the request content
def get_user_decorator(force_login=True):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            user = check_login(request)
            if not user and force_login:
                raise ServerError("user has not logged in")
            kwargs["user"] = user
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator

# Decorator for recording login failure messages
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

# Decorator for checking the number of false logins in a short period of time, enabling temporary banning of malicious access to ip addresses
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