import json
from django.http import HttpResponse
from .common import *

def get_region_list(request):
    sep = "#"
    response_data = {"region_list": sep.join(list(REGION2RID.keys())),
                     "separator": sep}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_currency_list(request):
    sep = "#"
    exchange_rate_list = list(CURRENCY2CID.keys())
    exchange_rate_list.sort()
    response_data = {"currency_list": sep.join(exchange_rate_list),
                     "separator": sep}
    return HttpResponse(json.dumps(response_data), content_type="application/json")