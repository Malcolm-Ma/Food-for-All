from Common.common import *

file_dir = {"img": IMG_DIR,
            "doc": DOC_DIR}

def gen_file_name(origin_name, file_type="img"):
    split_name = os.path.splitext(origin_name)
    file_name = split_name[0] + "." + str(time.time()).replace(".", "") + split_name[1]
    if os.path.isfile(os.path.join(file_dir[file_type], file_name)):
        return gen_file_name(origin_name, file_type)
    return file_name

def write_file_from_obj(file_name, file_obj, file_type="img", mode='wb'):
    path = os.path.join(file_dir[file_type], file_name)
    try:
        with open(path, mode) as f:
            for line in file_obj:
                f.write(line)
    except:
        raise ServerError("write to file failed")

def remove_url_file(url, file_type="img"):
    if url:
        path = os.path.join(file_dir[file_type], os.path.basename(url))
        try:
            if os.path.isfile(path):
                os.remove(path)
        except:
            logger_standard.warning("Remove {path} failed.".format(path=path))

def check_url_file_exist(url, file_type="img"):
    return os.path.isfile(os.path.join(file_dir[file_type], os.path.basename(url)))