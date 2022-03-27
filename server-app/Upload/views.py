from Common.common import *
from Common.utils import *
from Common.decorators import *

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
def upload_img(request):
    """
    @api {POST} /upload_img/ upload image
    @apiVersion 1.0.0
    @apiName upload_img
    @apiGroup Upload
    @apiDescription api to upload image file

    @apiParam {form-data} img Image file object

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [300005] write to file failed, [400002] unable to get image file from request)
    @apiSuccess (Success 200 return) {String} url Static url of image file just uploaded.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "url": "static/default_avatar.1647454464799235.jpg"
    }
    """
    response_data = {"status": STATUS_CODE["success"], "url": ""}
    file_obj = request.FILES.get('img')
    if not file_obj:
        raise ServerError("unable to get image file from request")
    file_name = gen_file_name(file_obj.name, "img")
    write_file_from_obj(file_name, file_obj, "img", 'wb')
    response_data["url"] = os.path.join(STATIC_URL, file_name)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
def upload_doc(request):
    """
    @api {POST} /upload_doc/ upload document
    @apiVersion 1.0.0
    @apiName upload_doc
    @apiGroup Upload
    @apiDescription api to upload document file

    @apiParam {form-data} doc Document file object

    @apiSuccess (Success 200 return) {Int} status Status code ([0]: success, [300005] write to file failed, [400003] unable to get document file from request)
    @apiSuccess (Success 200 return) {String} url Static url of document file just uploaded.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "url": "static/README.16474544716317701.md"
    }
    """
    response_data = {"status": STATUS_CODE["success"], "url": ""}
    file_obj = request.FILES.get('doc')
    if not file_obj:
        raise ServerError("unable to get document file from request")
    file_name = gen_file_name(file_obj.name, "doc")
    write_file_from_obj(file_name, file_obj, "doc", 'wb')
    response_data["url"] = os.path.join(STATIC_URL, file_name)
    return HttpResponse(json.dumps(response_data), content_type="application/json")