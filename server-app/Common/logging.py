import logging
from functools import wraps
from Login.functions import check_login
from Common.common import *

logger_standard = logging.getLogger('standard')

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