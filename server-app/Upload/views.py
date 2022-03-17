from django.http import HttpResponse, HttpResponseBadRequest
import json
from .functions import *

def upload_img(request):
    """
    @api {POST} /upload_img/ upload image
    @apiVersion 1.0.0
    @apiName upload_img
    @apiGroup Upload
    @apiDescription api to upload image file

    @apiParam {form-data} img Image file object

    @apiSuccess (200) {string} url Static url of image file just uploaded.

    @apiSuccessExample {Json} Response-Success
    {
        "url": "static/default_avatar.1647454464799235.jpg"
    }
    """
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {"url": ""}
    file_obj = request.FILES.get('img')
    file_name = gen_img_name(file_obj.name)
    img_path = os.path.join(IMG_PATH, file_name)
    write_file(img_path, file_obj, 'wb')
    response_data["url"] = os.path.join(STATIC_URL, file_name)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def upload_doc(request):
    """
    @api {POST} /upload_doc/ upload document
    @apiVersion 1.0.0
    @apiName upload_doc
    @apiGroup Upload
    @apiDescription api to upload document file

    @apiParam {form-data} doc Document file object

    @apiSuccess (200) {string} url Static url of document file just uploaded.

    @apiSuccessExample {Json} Response-Success
    {
        "url": "static/README.16474544716317701.md"
    }
    """
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {"url": ""}
    file_obj = request.FILES.get('doc')
    file_name = gen_doc_name(file_obj.name)
    doc_path = os.path.join(DOC_PATH, file_name)
    write_file(doc_path, file_obj, 'wb')
    response_data["url"] = os.path.join(STATIC_URL, file_name)
    return HttpResponse(json.dumps(response_data), content_type="application/json")