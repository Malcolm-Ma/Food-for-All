from .functions import *

class ServerError(Exception):
    def __init__(self, info):
        self.code = STATUS_CODE[info]

    def response(self):
        return HttpResponse(json.dumps({"status": self.code}), content_type="application/json")
