from .common import *
from Common.decorators import *

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["GET"])
def get_region_list(request):
    """
    @api {GET} /region_list/ region list
    @apiVersion 1.0.0
    @apiName region_list
    @apiGroup Common
    @apiDescription api to get country or region list

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success)
    @apiSuccess (Success 200 return) {List(Dict)} region_list Region list. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} region (Sub-parameter of region_list) Region full name.
    @apiSuccess (Success 200 return) {String} code (Sub-parameter of region_list) Region code.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "region_list": [
            {
                "region": "Afghanistan",
                "code": "AF"
            },
            {
                "region": "Albania",
                "code": "AL"
            },
            {
                "region": "Algeria",
                "code": "DZ"
            },
            {
                "region": "Andorra",
                "code": "AD"
            },
            {
                "region": "Angola",
                "code": "AO"
            },
            {
                "region": "Anguilla",
                "code": "AI"
            },
            ...
        ]
    }
    """
    region_list = [{"region": i, "code": j} for i, j in sorted(list(REGION2RID.items()), key=lambda x: x[0])]
    response_data = {"status": STATUS_CODE["success"], "region_list": region_list}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["GET"])
def get_currency_list(request):
    """
    @api {GET} /currency_list/ currency list
    @apiVersion 1.0.0
    @apiName currency_list
    @apiGroup Common
    @apiDescription api to get currency type list

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success)
    @apiSuccess (Success 200 return) {List(Dict)} currency_list Currency type list. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} currency_type (Sub-parameter of currency_list) Currency type full name.
    @apiSuccess (Success 200 return) {String} code (Sub-parameter of currency_list) Currency type code.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "currency_list": [
            {
                "currency_type": "Afghan Afghani",
                "code": "AFN"
            },
            {
                "currency_type": "Albanian Lek",
                "code": "ALL"
            },
            {
                "currency_type": "Algerian Dinar",
                "code": "DZD"
            },
            {
                "currency_type": "Angolan Kwanza",
                "code": "AOA"
            },
            {
                "currency_type": "Argentine Peso",
                "code": "ARS"
            },
            ...
        ]
    }
    """
    currency_list = [{"currency_type": i, "code": j} for i, j in sorted(list(CURRENCY2CID.items()), key=lambda x: x[0])]
    response_data = {"status": STATUS_CODE["success"], "currency_list": currency_list}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["GET"])
def get_region2currency(request):
    """
    @api {GET} /region2currency/ region to currency
    @apiVersion 1.0.0
    @apiName region2currency
    @apiGroup Common
    @apiDescription api to get dict region: default currency type

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success)
    @apiSuccess (Success 200 return) {Dict} region2currency Matching regions' codes and their default currency types with format{string: string}, i.e.{region_code: default_currency_type_code}.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "region2currency": {
            "AE": "AED",
            "AF": "AFN",
            "AL": "ALL",
            "AM": "AMD",
            "AN": "ANG",
            "CW": "ANG",
            "AO": "AOA",
            "AR": "ARS",
            "AU": "AUD",
            ...
        }
    }
    """
    response_data = {"status": STATUS_CODE["success"], "region2currency": RID2CID}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
