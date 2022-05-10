import time
import requests
import json
from pathlib import Path
import re
import os
import pymysql
from hashlib import md5
import csv
import base64 as b64

#mail = "test@example.com"
#mail = "ty_liang@foxmail.com"
mail = input("Input email address you are using: ")

password = b64.b64encode("123456".encode()).decode()
reset_password = b64.b64encode("111111".encode()).decode()

path = Path(__file__).resolve().parent
output_file = os.path.join(path, "test_backend_result.txt")

mysql_host = '127.0.0.1'
mysql_user='apex'
mysql_password='apex08'
mysql_port=3306
mysql_db='foodforall'
def get_all_cursor_dict(cursor):
    data_ori = cursor.fetchall()
    data_list = []
    for i in range(len(data_ori)):
        data_dict = {}
        for j in range(len(cursor.description)):
            data_dict[cursor.description[j][0]] = data_ori[i][j]
        data_list.append(data_dict)
    return data_list
def get_one_cursor_dict(cursor):
    data_ori = cursor.fetchone()
    data_dict = {}
    for i in range(len(cursor.description)):
        data_dict[cursor.description[i][0]] = data_ori[i]
    return data_dict

rs = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

STATUS_CODE = {"success": 0,
               "user has not logged in": 100001,
               "user update failed": 100002,
               "operation is not available to individual user": 100003,
               "user is already logged in": 100004,
               "invalid username": 100005,
               "wrong password": 100006,
               "email is already registered": 100007,
               "password setting failed": 100008,
               "email is not registered": 100009,
               "mismatch between logged in user and target user": 100010,
               "invalid user type": 100011,
               "wrong parameters for user creation": 100012,
               "user creation failed": 100013,
               "target user does not exist": 100014,
               "project creation failed": 200001,
               "project does not exist": 200002,
               "user is not the owner of the project": 200003,
               "project is not deletable": 200004,
               "project update failed": 200005,
               "project is not editable": 200006,
               "project information is incomplete": 200007,
               "project start up failed": 200008,
               "project has already started": 200009,
               "project stop failed": 200010,
               "project is not ongoing or on hold": 200011,
               "project end time is invalid": 200012,
               "project status invalid": 200013,
               "project price invalid": 200014,
               "project order invalid": 200015,
               "project is aiready finished": 200016,
               "project is not ongoing": 200017,
               "project suspension failed": 200018,
               "invalid currency type": 300001,
               "email delivery failed": 300002,
               "captcha verification failed": 300003,
               "invalid action": 300004,
               "write to file failed": 300005,
               "wrong region name or code": 300006,
               "invalid request parameters": 400001,
               "unable to get image file from request": 400002,
               "unable to get document file from request": 400003,
               "temporary ban due to too frequent login attempts": 400004,
               "create paypal product failed": 500001,
               "payment capture failed": 500002,
               }

main_url = "http://127.0.0.1:8000/"
api_list = ['init_database/', 'region_list/', 'currency_list/', 'region2currency/', 'upload_img/', 'upload_doc/', 'share_by_email/', 'get_ip_info/',
            'login/', 'regis/', 'logout/', 'reset_password/', 'get_user/', 'edit_user/',
            'get_project/', 'edit_project/', 'get_projects_list/', 'get_prepare_projects_list/',
            'create_project/', 'delete_project/', 'start_project/', 'suspend_project/', 'stop_project/', ]
url_dict = {}
for api in api_list:
    url_dict[api] = os.path.join(main_url, api)

correct_response = {}
for api in api_list:
    correct_response[api] = {}
correct_response['init_database/'][STATUS_CODE["success"]] = []
#correct_response['init_database/'][STATUS_CODE["success"]] = [["POST", {"user_num": 10, "project_num": 20}, '{"user_num": 10, "project_num": 20, "user_list": .*}']]
correct_response['init_database/'][STATUS_CODE["success"]].append(["GET", "", '{"user_num": [0-9]+, "project_num": [0-9]+, "user_list": .*}'])
correct_response['region_list/'][STATUS_CODE["success"]] = [["GET", "", '{"status": 0, "region_list": .*}']]
correct_response['currency_list/'][STATUS_CODE["success"]] = [["GET", "", '{"status": 0, "currency_list": .*}']]
correct_response['region2currency/'][STATUS_CODE["success"]] = [["GET", "", '{"status": 0, "region2currency": {.*}']]

def get_response(url, method, data):
    if method == "GET":
        r = rs.get(url, headers=headers)
    elif method == "POST":
        r = rs.post(url, headers=headers, data=json.dumps(data))
    return r.text

def check_api(api, code, method, data, answer):
    code = str(code)
    response = get_response(url_dict[api], method, data)
    if response == answer:
        result = "Success"
    elif len(re.findall(answer, response)) == 1:
        result = "Success"
    else:
        result = "Fail"
    result_text = "[{result:<7s}] - [{api:<30s}] - [{method:<4s}] - [{code:<6s}]".format(result=result, api=api, method=method, code=code)
    print(result_text)
    if result == "Fail":
        print("Response: " + response)
        print("Answer  : " + answer)
    time.sleep(0.1)
    return result_text

def check_wrong_request_method():
    r = rs.get(url_dict["login/"], headers=headers)
    if r.status_code == 405:
        result = "Success"
    else:
        result = "Fail"
    result_text = "[{result:<7s}] - [{api:<30s}] - [{method:<4s}] - [{code:<6s}]".format(result=result, api="405",
                                                                                        method="GET", code="405")
    print(result_text)
    return result_text

def check_wrong_request_params():
    r = rs.post(url_dict["login/"], headers=headers, data=json.dumps({}))
    if r.status_code == 400:
        result = "Success"
    else:
        result = "Fail"
    result_text = "[{result:<7s}] - [{api:<30s}] - [{method:<4s}] - [{code:<6s}]".format(result=result, api="400",
                                                                                        method="POST", code="400")
    print(result_text)
    return result_text

def check_upload(api, key, file):
    if file:
        with open(file, "rb") as f:
            r = rs.post(url_dict[api], headers=headers, files={"files": f, 'Content-Type': 'multipart/form-data'})
        if len(re.findall(r'{"status": 0, "url": "static/.+"}', r.text)) == 1:
            result = "Success"
        else:
            result = "Fail"
        result_text = "[{result:<7s}] - [{api:<30s}] - [{method:<4s}] - [{code:<6s}]".format(result=result, api=api,
                                                                                             method="POST", code="0")
    else:
        code_dict = {"img": "400002", "doc": "400003"}
        r = rs.post(url_dict[api], headers=headers)
        if len(re.findall(r'{"status": %s}' % code_dict[key], r.text)) == 1:
            result = "Success"
        else:
            result = "Fail"
        result_text = "[{result:<7s}] - [{api:<30s}] - [{method:<4s}] - [{code:<6s}]".format(result=result, api=api,
                                                                                             method="POST", code=code_dict[key])
    print(result_text)
    return result_text

def user_login(username, password):
    r = rs.post(url_dict["login/"], headers=headers, data=json.dumps({"username": username, "password": password}))
    return r

def user_logout():
    r = rs.get(url_dict["logout/"], headers=headers)
    return r

def create_project():
    r = rs.get(url_dict["create_project/"], headers=headers)
    return r

#def gen_verify_code(id_str, usefor_str, expires=30 * 60):
#    dynamic_num = int(time.time()) // expires
#    code = md5((str(dynamic_num) + id_str + usefor_str).encode("utf-8")).hexdigest()[:6]
#    return code

if __name__ == "__main__":
    with pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port, db=mysql_db) as db:
        with db.cursor() as cursor:
            with open(output_file, "w") as f:
                f.write(check_wrong_request_method() + "\n")
                f.write(check_wrong_request_params() + "\n")
                f.write(check_upload('upload_img/', 'img', os.path.join(path, "test.jpg")) + "\n")
                f.write(check_upload('upload_img/', 'img', "") + "\n")
                f.write(check_upload('upload_doc/', 'doc', os.path.join(path, "test.txt")) + "\n")
                f.write(check_upload('upload_doc/', 'doc', "") + "\n")
                #300005 can't be test
                for api in ['init_database/', 'region_list/', 'currency_list/', 'region2currency/']:
                    for code in correct_response[api]:
                        for method, data, answer in correct_response[api][code]:
                            f.write(check_api(api, code, method, data, answer) + "\n")
                with open(os.path.join(path, "init_database_user.csv"), "r", encoding='utf-8', newline='') as uf:
                    user_list = list(csv.DictReader(uf))
                cursor.execute('SELECT * FROM database_duser WHERE type=1 AND project!=""')
                db.commit()
                user = get_one_cursor_dict(cursor)
                for i in user_list:
                    if i["uid"] == user["uid"]:
                        user["password"] = i["encrypted_password"]
                        break

                f.write(check_api('get_ip_info/', "", "GET", "", '{"status":"fail","message":"reserved range","query":"127.0.0.1"}') + "\n")
                f.write(check_api('login/', STATUS_CODE["invalid username"], "POST", {"username": "test" + user["mail"], "password": user["password"]}, '{"status": %d}' % STATUS_CODE["invalid username"]) + "\n")
                f.write(check_api('login/', STATUS_CODE["wrong password"], "POST", {"username": user["mail"], "password": b64.b64encode("test".encode()).decode()}, '{"status": %d}' % STATUS_CODE["wrong password"]) + "\n")
                f.write(check_api('login/', STATUS_CODE["success"], "POST", {"username": user["mail"], "password": user["password"]}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('login/', STATUS_CODE["user is already logged in"], "POST", {"username": user["mail"], "password": user["password"]}, '{"status": %d}' % STATUS_CODE["user is already logged in"]) + "\n")

                f.write(check_api('logout/', STATUS_CODE["success"], "GET", "", '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('logout/', STATUS_CODE["user has not logged in"], "GET", "", '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")

                f.write(check_api('regis/', STATUS_CODE["invalid action"], "POST", {"username": user["mail"], "action": 4}, '{"status": %d, "action": 4}' % STATUS_CODE["invalid action"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["email is already registered"], "POST", {"username": user["mail"], "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["email is already registered"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["email delivery failed"], "POST", {"username": "test", "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["email delivery failed"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["success"], "POST", {"username": mail, "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["captcha verification failed"], "POST", {"username": mail, "action": 1, "code": "testtest"}, '{"status": %d, "action": 1}' % STATUS_CODE["captcha verification failed"]) + "\n")
                #code = gen_verify_code(mail, "regis")
                code = input("Input registration verification code: ")
                f.write(check_api('regis/', STATUS_CODE["success"], "POST", {"username": mail, "action": 1, "code": code}, '{"status": %d, "action": 1}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["wrong parameters for user creation"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "CN", "currency_type": "GBP", "name": "tyl", "avatar": ""}, '{"status": %d, "action": 2}' % STATUS_CODE["wrong parameters for user creation"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["invalid user type"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "CN", "currency_type": "GBP", "name": "tyl", "avatar": "", "type": 9, "hide": 0}, '{"status": %d, "action": 2}' % STATUS_CODE["invalid user type"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["wrong region name or code"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "testCN", "currency_type": "GBP", "name": "tyl", "avatar": "", "type": 2, "hide": 0}, '{"status": %d, "action": 2}' % STATUS_CODE["wrong region name or code"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["invalid currency type"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "CN", "currency_type": "testGBP", "name": "tyl", "avatar": "", "type": 2, "hide": 0}, '{"status": %d, "action": 2}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["success"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "CN", "currency_type": "GBP", "name": "tyl", "avatar": "", "type": 2, "hide": 0}, '{"status": %d, "action": 2}' % STATUS_CODE["success"]) + "\n")
                user_login(mail, password)
                f.write(check_api('regis/', STATUS_CODE["user is already logged in"], "POST", {"username": mail, "action": 0}, '{"status": %d.*}' % STATUS_CODE["user is already logged in"]) + "\n")
                #100013 can't be test

                f.write(check_api('reset_password/', STATUS_CODE["invalid action"], "POST", {"username": mail, "action": 4}, '{"status": %d, "action": 4}' % STATUS_CODE["invalid action"]) + "\n")
                f.write(check_api('reset_password/', STATUS_CODE["mismatch between logged in user and target user"], "POST", {"username": user["mail"], "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["mismatch between logged in user and target user"]) + "\n")
                f.write(check_api('reset_password/', STATUS_CODE["success"], "POST", {"username": mail, "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('reset_password/', STATUS_CODE["captcha verification failed"], "POST", {"username": mail, "action": 1, "code": "testtest"}, '{"status": %d, "action": 1}' % STATUS_CODE["captcha verification failed"]) + "\n")
                #code = gen_verify_code(mail, "reset_password")
                code = input("Input reset password verification code: ")
                f.write(check_api('reset_password/', STATUS_CODE["success"], "POST", {"username": mail, "action": 1, "code": code}, '{"status": %d, "action": 1}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('reset_password/', STATUS_CODE["success"], "POST", {"username": mail, "action": 2, "code": code, "password": reset_password}, '{"status": %d, "action": 2}' % STATUS_CODE["success"]) + "\n")
                user_logout()
                f.write(check_api('reset_password/', STATUS_CODE["email is not registered"], "POST", {"username": "test" + mail, "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["email is not registered"]) + "\n")
                #100008, 300002 can't be test

                f.write(check_api('get_user/', STATUS_CODE["user has not logged in"], "GET", "", '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                user_login(user["mail"], user["password"])
                f.write(check_api('get_user/', STATUS_CODE["target user does not exist"], "POST", {"uid": "test" + user["uid"]}, '{"status": %d}' % STATUS_CODE["target user does not exist"]) + "\n")
                f.write(check_api('get_user/', STATUS_CODE["success"], "GET", "", '{"status": %d, "user_info": {"uid": "%s", "mail": "%s", .*}' % (STATUS_CODE["success"], user["uid"], user["mail"])) + "\n")

                f.write(check_api('edit_user/', STATUS_CODE["invalid currency type"], "POST", {"name": "test", "region": "AL", "currency_type": "testUSD", "avatar": ""}, '{"status": %d}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('edit_user/', STATUS_CODE["wrong region name or code"], "POST", {"name": "test", "region": "testAL", "currency_type": "USD", "avatar": ""}, '{"status": %d}' % STATUS_CODE["wrong region name or code"]) + "\n")
                f.write(check_api('edit_user/', STATUS_CODE["success"], "POST", {"name": "test", "region": "AL", "currency_type": "USD", "avatar": ""}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                user_logout()
                f.write(check_api('edit_user/', STATUS_CODE["user has not logged in"], "POST", {"name": "test", "region": "AL", "currency_type": "USD", "avatar": ""}, '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                #100002 can't be test

                f.write(check_api('create_project/', STATUS_CODE["user has not logged in"], "GET", "", '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('create_project/', STATUS_CODE["operation is not available to individual user"], "GET", "", '{"status": %d}' % STATUS_CODE["operation is not available to individual user"]) + "\n")
                user_logout()
                user_login(user["mail"], user["password"])
                f.write(check_api('create_project/', STATUS_CODE["success"], "GET", "", '{"status": %d, "pid": "[0-9a-z]*"}' % STATUS_CODE["success"]) + "\n")
                #200001 can't be test

                cursor.execute('SELECT * FROM database_dproject WHERE uid="{uid}" AND status=0 AND title=""'.format(uid=user["uid"]))
                db.commit()
                project = get_one_cursor_dict(cursor)
                f.write(check_api('edit_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) + 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                f.write(check_api('edit_project/', STATUS_CODE["invalid currency type"], "POST", {"pid": project["pid"], "currency_type": "CNYTEST", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) + 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('edit_project/', STATUS_CODE["project end time is invalid"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) - 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["project end time is invalid"]) + "\n")
                user_logout()
                f.write(check_api('edit_project/', STATUS_CODE["user has not logged in"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) - 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('edit_project/', STATUS_CODE["user is not the owner of the project"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) - 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["user is not the owner of the project"]) + "\n")
                #200005 can't be test

                f.write(check_api('start_project/', STATUS_CODE["user is not the owner of the project"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not the owner of the project"]) + "\n")
                user_logout()
                f.write(check_api('start_project/', STATUS_CODE["user has not logged in"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                user_login(user["mail"], user["password"])
                f.write(check_api('start_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"]}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                f.write(check_api('start_project/', STATUS_CODE["project information is incomplete"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project information is incomplete"]) + "\n")
                f.write(check_api('edit_project/', STATUS_CODE["project price invalid"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) + 24 * 60 * 60, "details": "apex", "price": -100}}, '{"status": %d}' % STATUS_CODE["project price invalid"]) + "\n")
                f.write(check_api('edit_project/', STATUS_CODE["success"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) + 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('start_project/', STATUS_CODE["success"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('edit_project/', STATUS_CODE["project is not editable"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) - 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["project is not editable"]) + "\n")
                f.write(check_api('start_project/', STATUS_CODE["project has already started"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project has already started"]) + "\n")
                #200008, 200016 can't be test

                f.write(check_api('suspend_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"]}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                user_logout()
                f.write(check_api('suspend_project/', STATUS_CODE["user has not logged in"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('suspend_project/', STATUS_CODE["user is not the owner of the project"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not the owner of the project"]) + "\n")
                user_logout()
                user_login(user["mail"], user["password"])
                f.write(check_api('suspend_project/', STATUS_CODE["success"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('suspend_project/', STATUS_CODE["project is not ongoing"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project is not ongoing"]) + "\n")
                #200016, 200018 can't be test
                
                f.write(check_api('stop_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"]}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                user_logout()
                f.write(check_api('stop_project/', STATUS_CODE["user has not logged in"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('stop_project/', STATUS_CODE["user is not the owner of the project"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not the owner of the project"]) + "\n")
                user_logout()
                user_login(user["mail"], user["password"])
                f.write(check_api('stop_project/', STATUS_CODE["success"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('stop_project/', STATUS_CODE["project is not ongoing or on hold"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project is not ongoing or on hold"]) + "\n")
                #200010, 200016 can't be test

                f.write(check_api('delete_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"]}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                f.write(check_api('delete_project/', STATUS_CODE["project is not deletable"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project is not deletable"]) + "\n")
                user_logout()
                f.write(check_api('delete_project/', STATUS_CODE["user has not logged in"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('delete_project/', STATUS_CODE["user is not the owner of the project"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not the owner of the project"]) + "\n")
                user_logout()
                user_login(user["mail"], user["password"])
                create_project()
                cursor.execute('SELECT * FROM database_dproject WHERE uid="{uid}" AND status=0'.format(uid=user["uid"]))
                db.commit()
                project_tmp = get_one_cursor_dict(cursor)
                f.write(check_api('delete_project/', STATUS_CODE["success"], "POST", {"pid": project_tmp["pid"]}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")

                f.write(check_api('get_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"], "currency_type": "CNY"}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                f.write(check_api('get_project/', STATUS_CODE["invalid currency type"], "POST", {"pid": project["pid"], "currency_type": "testCNY"}, '{"status": %d}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('get_project/', STATUS_CODE["success"], "POST", {"pid": project["pid"], "currency_type": "CNY"}, '{"status": %d, "project_info": {"pid": "%s", "uid": "%s", .*}' % (STATUS_CODE["success"], project["pid"], project["uid"])) + "\n")

                create_project()
                f.write(check_api('get_prepare_projects_list/', STATUS_CODE["invalid currency type"], "POST", {"currency_type": "testCNY", "page_info": {"page_size": 3, "page": 1}, "search": ""}, '{"status": %d.*}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('get_prepare_projects_list/', STATUS_CODE["success"], "POST", {"currency_type": "CNY", "page_info": {"page_size": 3, "page": 1}, "search": "q"}, '{"status": %d.*}' % STATUS_CODE["success"]) + "\n")
                user_logout()
                f.write(check_api('get_prepare_projects_list/', STATUS_CODE["user has not logged in"], "POST", {"currency_type": "CNY", "page_info": {"page_size": 3, "page": 1}, "search": "q"}, '{"status": %d}' % STATUS_CODE["user has not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('get_prepare_projects_list/', STATUS_CODE["operation is not available to individual user"], "POST", {"currency_type": "CNY", "page_info": {"page_size": 3, "page": 1}, "search": "q"}, '{"status": %d}' % STATUS_CODE["operation is not available to individual user"]) + "\n")

                f.write(check_api('get_projects_list/', STATUS_CODE["project order invalid"], "POST", {"order": "-testprogress", "currency_type": "CNY", "page_info": {"page_size": 5, "page": 1}, "search": "", "valid_only": 1, "uid": ""}, '{"status": %d}' % STATUS_CODE["project order invalid"]) + "\n")
                f.write(check_api('get_projects_list/', STATUS_CODE["invalid currency type"], "POST", {"order": "-progress", "currency_type": "testCNY", "page_info": {"page_size": 5, "page": 1}, "search": "", "valid_only": 1, "uid": ""}, '{"status": %d}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('get_projects_list/', STATUS_CODE["success"], "POST", {"order": "-progress", "currency_type": "CNY", "page_info": {"page_size": 5, "page": 1}, "search": "", "valid_only": 1, "uid": ""}, '{"status": %d.*}' % STATUS_CODE["success"]) + "\n")

                f.write(check_api('share_by_email/', STATUS_CODE["success"], "POST", {"mail": [mail], "project_name": "qwer", "project_url": "http://127.0.0.1:3000", "donate_num": 3, "if_hide_personal_information": 0, "user_name": "test"}, '{"status": %d.*}' % STATUS_CODE["success"]) + "\n")
                
                for _ in range(10):
                    user_login("test", b64.b64encode("test".encode()).decode())
                f.write(check_api('login/', STATUS_CODE["temporary ban due to too frequent login attempts"], "POST", {"username": "test" + user["mail"], "password": user["password"]}, '{"status": %d}' % STATUS_CODE["temporary ban due to too frequent login attempts"]) + "\n")
                