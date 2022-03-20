import time
from Common.common import *

def write_file(file_path, file_obj, mode='wb'):
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