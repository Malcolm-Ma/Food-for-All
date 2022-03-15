from django.http import HttpResponse
import json
from .functions import *

def upload_img(request):
    response_data = {"url": ""}
    file_obj = request.FILES.get('img')
    file_name = gen_img_name(file_obj.name)
    img_path = os.path.join(IMG_PATH, file_name)
    write_file(img_path, file_obj, 'wb')
    response_data["url"] = os.path.join(STATIC_URL, file_name)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def upload_doc(request):
    response_data = {"url": ""}
    file_obj = request.FILES.get('doc')
    file_name = gen_doc_name(file_obj.name)
    doc_path = os.path.join(DOC_PATH, file_name)
    write_file(doc_path, file_obj, 'wb')
    response_data["url"] = os.path.join(STATIC_URL, file_name)
    return HttpResponse(json.dumps(response_data), content_type="application/json")