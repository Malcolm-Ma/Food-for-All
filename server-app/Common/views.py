import json
from django.http import HttpResponse
from .common import *

def get_region_list(request):
    """
    @api {GET} /region_list/ region list
    @apiVersion 1.0.0
    @apiName region_list
    @apiGroup Common
    @apiDescription api to get country or region list

    @apiSuccess (200) {list(string)} region_list Region list.

    @apiSuccessExample {Json} Response-Success
    {
        "region_list": [
            "Afghanistan",
            "Albania",
            "Algeria",
            "Andorra",
            "Angola",
            "Anguilla",
            "Antigua and Barbuda",
            "Arab Emirates",
            "Argentina",
            "Armenia",
            "Aruba",
            "Australia",
            "Austria",
            ...
        ]
    }
    """
    response_data = {"region_list": sorted(list(REGION2RID.keys()))}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_currency_list(request):
    """
    @api {GET} /currency_list/ currency list
    @apiVersion 1.0.0
    @apiName currency_list
    @apiGroup Common
    @apiDescription api to get currency type list

    @apiSuccess (200) {list(string)} currency_list Currency type list.

    @apiSuccessExample {Json} Response-Success
    {
        "currency_list": [
            "AED (Emirati Dirham)",
            "AFN (Afghan Afghani)",
            "ALL (Albanian Lek)",
            "AMD (Armenian Dram)",
            "ANG (Dutch Guilder)",
            "AOA (Angolan Kwanza)",
            "ARS (Argentine Peso)",
            "AUD (Australian Dollar)",
            "AWG (Aruban or Dutch Guilder)",
            "AZN (Azerbaijan Manat)",
            "BAM (Bosnian Convertible Mark)",
            "BBD (Barbadian or Bajan Dollar)",
            "BDT (Bangladeshi Taka)",
            ...
        ]
    }
    """
    response_data = {"currency_list": sorted(list(CURRENCY2CID.keys()))}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_region2currency(request):
    """
    @api {GET} /region2currency/ region to currency
    @apiVersion 1.0.0
    @apiName region2currency
    @apiGroup Common
    @apiDescription api to get dict region: default currency type

    @apiSuccess (200) {dict} region2currency Matching regions and their default currency type with format{string: string}, i.e.{region: default_currency_type}.

    @apiSuccessExample {Json} Response-Success
    {
        "region2currency": {
            "Arab Emirates": "AED (Emirati Dirham)",
            "Afghanistan": "AFN (Afghan Afghani)",
            "Albania": "ALL (Albanian Lek)",
            "Armenia": "AMD (Armenian Dram)",
            "Netherlands Antilles": "ANG (Dutch Guilder)",
            "Curacao": "ANG (Dutch Guilder)",
            "Angola": "AOA (Angolan Kwanza)",
            "Argentina": "ARS (Argentine Peso)",
            "Australia": "AUD (Australian Dollar)",
            ...
        }
    }
    """
    response_data = {"region2currency": REGION2CURRENCY}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
