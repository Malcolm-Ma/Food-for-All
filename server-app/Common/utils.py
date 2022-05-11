from Common.common import *

# The code in this script contains the definitions of some generic functions that are dependencies of some of the project code

file_dir = {"img": IMG_DIR,
            "doc": DOC_DIR}

# Function for generating filename
def gen_file_name(origin_name, file_type="img"):
    split_name = os.path.splitext(origin_name)
    file_name = split_name[0] + "." + str(time.time()).replace(".", "") + split_name[1]
    if os.path.isfile(os.path.join(file_dir[file_type], file_name)):
        return gen_file_name(origin_name, file_type)
    return file_name

# Function for writing out files
def write_file_from_obj(file_name, file_obj, file_type="img", mode='wb'):
    path = os.path.join(file_dir[file_type], file_name)
    try:
        with open(path, mode) as f:
            for line in file_obj:
                f.write(line)
    except:
        raise ServerError("write to file failed")

# Function for deleting some expired files to avoid the accumulation of redundant files taking up server resources.
def remove_url_file(url, file_type="img"):
    if url:
        path = os.path.join(file_dir[file_type], os.path.basename(url))
        try:
            if os.path.isfile(path):
                os.remove(path)
        except:
            logger_standard.warning("Remove {path} failed.".format(path=path))

# Function to detect the existence of a file
def check_url_file_exist(url, file_type="img"):
    return os.path.isfile(os.path.join(file_dir[file_type], os.path.basename(url)))