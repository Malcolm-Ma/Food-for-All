from .functions import *

def get_request_url(request):
    url = request.META.get('HTTP_X_FORWARDED_FOR')
    if not url:
        url = request.META.get('REMOTE_ADDR')
    return url

def remove_img_file(img_url):
    if img_url:
        img_path = os.path.join(IMG_DIR, os.path.basename(img_url))
        if os.path.exists(img_path):
            os.remove(img_path)

def check_img_exist(img_url):
    return os.path.isfile(os.path.join(IMG_DIR, os.path.basename(img_url)))

def write_file_from_obj(file_path, file_obj, mode='wb'):
    with open(file_path, mode) as f:
        for line in file_obj:
            f.write(line)

def gen_img_name(origin_name):
    split_name = os.path.splitext(origin_name)
    file_name = split_name[0] + "." + str(time.time()).replace(".", "") + split_name[1]
    if os.path.isfile(os.path.join(IMG_DIR, file_name)):
        file_name = gen_img_name(origin_name)
    return file_name

def gen_doc_name(origin_name):
    split_name = os.path.splitext(origin_name)
    file_name = split_name[0] + "." + str(time.time()).replace(".", "") + split_name[1]
    if os.path.isfile(os.path.join(DOC_DIR, file_name)):
        file_name = gen_doc_name(origin_name)
    return file_name