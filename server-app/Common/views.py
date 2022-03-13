import json
from django.http import HttpResponse
from FoodForAll.settings import REGION2RID, RID2REGION, EXCHANGE_RATE, CURRENCY2CID, CID2CURRENCY

def get_region(request):
    sep = "#"
    response_data = {"region_list": sep.join(list(REGION2RID.keys())),
                     "separator": sep}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_currency(request):
    sep = "#"
    exchange_rate_list = list(CURRENCY2CID.keys())
    exchange_rate_list.sort()
    response_data = {"currency_list": sep.join(exchange_rate_list),
                     "separator": sep}
    return HttpResponse(json.dumps(response_data), content_type="application/json")