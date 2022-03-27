import time
import requests
import json
from pathlib import Path
import re
import os
import pymysql
from hashlib import md5
import csv

#mail = "ty_liang@foxmail.com"
mail = input("Input email address you are using: ")
password = "123456"
reset_password = "111111"

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
               "user is not logged in": 100001,
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
               "project is not ongoing": 200011,
               "project end time is invalid": 200012,
               "project status invalid": 200013,
               "project price invalid": 200014,
               "project order invalid": 200015,
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
               }

main_url = "http://127.0.0.1:8000/"
api_list = ['init_database/', 'region_list/', 'currency_list/', 'region2currency/', 'upload_img/', 'upload_doc/',
            'login/', 'regis/', 'logout/', 'reset_password/', 'get_user/', 'edit_user/',
            'get_project/', 'edit_project/', 'get_projects_list/', 'get_prepare_projects_list/',
            'create_project/', 'delete_project/', 'start_project/', 'stop_project/', ]
url_dict = {}
for api in api_list:
    url_dict[api] = os.path.join(main_url, api)

correct_response = {}
for api in api_list:
    correct_response[api] = {}
correct_response['init_database/'][STATUS_CODE["success"]] = []
#correct_response['init_database/'][STATUS_CODE["success"]] = [["POST", {"user_num": 10, "project_num": 20}, '{"user_num": 10, "project_num": 20, "user_list": .*}']]
correct_response['init_database/'][STATUS_CODE["success"]].append(["GET", "", '{"user_num": [0-9]+, "project_num": [0-9]+, "user_list": .*}'])
correct_response['region_list/'][STATUS_CODE["success"]] = [["GET", "", '{"status": 0, "region_list": [{"region": "Afghanistan", "code": "AF"}, {"region": "Albania", "code": "AL"}, {"region": "Algeria", "code": "DZ"}, {"region": "Andorra", "code": "AD"}, {"region": "Angola", "code": "AO"}, {"region": "Anguilla", "code": "AI"}, {"region": "Antigua and Barbuda", "code": "AG"}, {"region": "Arab Emirates", "code": "AE"}, {"region": "Argentina", "code": "AR"}, {"region": "Armenia", "code": "AM"}, {"region": "Aruba", "code": "AW"}, {"region": "Australia", "code": "AU"}, {"region": "Austria", "code": "AT"}, {"region": "Azerbaijan", "code": "AZ"}, {"region": "Bahamas", "code": "BS"}, {"region": "Bahrain", "code": "BH"}, {"region": "Bangladesh", "code": "BD"}, {"region": "Barbados", "code": "BB"}, {"region": "Belarus", "code": "BY"}, {"region": "Belgium", "code": "BE"}, {"region": "Belize", "code": "BZ"}, {"region": "Benin", "code": "BJ"}, {"region": "Bermuda", "code": "BM"}, {"region": "Bhutan", "code": "BT"}, {"region": "Bolivia", "code": "BO"}, {"region": "Bosnia and Herzegovina", "code": "BA"}, {"region": "Botswana", "code": "BW"}, {"region": "Bouvet Island", "code": "BV"}, {"region": "Brazil", "code": "BR"}, {"region": "Brunei", "code": "BN"}, {"region": "Bulgaria", "code": "BG"}, {"region": "Burkina Faso", "code": "BF"}, {"region": "Burundi", "code": "BI"}, {"region": "Cambodia", "code": "KH"}, {"region": "Cameroon", "code": "CM"}, {"region": "Canada", "code": "CA"}, {"region": "Cape Verde", "code": "CV"}, {"region": "Cayman Islands", "code": "KY"}, {"region": "Central African Republic", "code": "CF"}, {"region": "Chad", "code": "TD"}, {"region": "Chile", "code": "CL"}, {"region": "China, Hong Kong S.A.R.", "code": "HK"}, {"region": "China, the People\'s Republic of China (PRC)", "code": "CN"}, {"region": "Cocos Islands", "code": "CC"}, {"region": "Colombia", "code": "CO"}, {"region": "Comoros", "code": "KM"}, {"region": "Congo", "code": "CG"}, {"region": "Congo, Democratic Republic of the Congo", "code": "CD"}, {"region": "Cook Islands", "code": "CK"}, {"region": "Costa Rica", "code": "CR"}, {"region": "Croatia", "code": "HR"}, {"region": "Cuba", "code": "CU"}, {"region": "Curacao", "code": "CW"}, {"region": "Cyprus", "code": "CY"}, {"region": "Czech Republic", "code": "CZ"}, {"region": "Denmark", "code": "DK"}, {"region": "Djibouti", "code": "DJ"}, {"region": "Dominica", "code": "DM"}, {"region": "Dominican Republic", "code": "DO"}, {"region": "Ecuador", "code": "EC"}, {"region": "Egypt", "code": "EG"}, {"region": "El Salvador", "code": "SV"}, {"region": "Equatorial Guinea", "code": "GQ"}, {"region": "Eritrea", "code": "ER"}, {"region": "Estonia", "code": "EE"}, {"region": "Ethiopia", "code": "ET"}, {"region": "Falkland Islands (Malvinas)", "code": "FK"}, {"region": "Faroe Islands", "code": "FO"}, {"region": "Fiji", "code": "FJ"}, {"region": "Finland", "code": "FI"}, {"region": "France", "code": "FR"}, {"region": "French Guiana", "code": "GF"}, {"region": "French Polynesia", "code": "PF"}, {"region": "Gabon", "code": "GA"}, {"region": "Gambia", "code": "GM"}, {"region": "Georgia, Republic of Georgia", "code": "GE"}, {"region": "Germany", "code": "DE"}, {"region": "Ghana", "code": "GH"}, {"region": "Gibraltar", "code": "GI"}, {"region": "Greece", "code": "GR"}, {"region": "Greenland", "code": "GL"}, {"region": "Grenada", "code": "GD"}, {"region": "Guadeloupe", "code": "GP"}, {"region": "Guatemala", "code": "GT"}, {"region": "Guernsey", "code": "GG"}, {"region": "Guinea", "code": "GN"}, {"region": "Guinea-Bissau", "code": "GW"}, {"region": "Guyana", "code": "GY"}, {"region": "Haiti", "code": "HT"}, {"region": "Honduras", "code": "HN"}, {"region": "Hungary", "code": "HU"}, {"region": "Iceland", "code": "IS"}, {"region": "India", "code": "IN"}, {"region": "Indonesia", "code": "ID"}, {"region": "Iran", "code": "IR"}, {"region": "Iraq", "code": "IQ"}, {"region": "Ireland", "code": "IE"}, {"region": "Isle of Man", "code": "IM"}, {"region": "Israel", "code": "IL"}, {"region": "Italy", "code": "IT"}, {"region": "Ivory Coast", "code": "CI"}, {"region": "Jamaica", "code": "JM"}, {"region": "Japan", "code": "JP"}, {"region": "Jersey", "code": "JE"}, {"region": "Jordan", "code": "JO"}, {"region": "Kazakhstan", "code": "KZ"}, {"region": "Kenya", "code": "KE"}, {"region": "Kiribati", "code": "KI"}, {"region": "Kuwait", "code": "KW"}, {"region": "Kyrgyzstan", "code": "KG"}, {"region": "Laos", "code": "LA"}, {"region": "Latvia", "code": "LV"}, {"region": "Lebanon", "code": "LB"}, {"region": "Lesotho", "code": "LS"}, {"region": "Liberia", "code": "LR"}, {"region": "Libya", "code": "LY"}, {"region": "Liechtenstein", "code": "LI"}, {"region": "Lithuania", "code": "LT"}, {"region": "Luxembourg", "code": "LU"}, {"region": "Macau", "code": "MO"}, {"region": "Macedonia (Former Yugoslav Republic)", "code": "MK"}, {"region": "Madagascar", "code": "MG"}, {"region": "Malawi", "code": "MW"}, {"region": "Malaysia", "code": "MY"}, {"region": "Maldives", "code": "MV"}, {"region": "Mali", "code": "ML"}, {"region": "Malta", "code": "MT"}, {"region": "Marshall Islands", "code": "MH"}, {"region": "Martinique", "code": "MQ"}, {"region": "Mauritania", "code": "MR"}, {"region": "Mauritius", "code": "MU"}, {"region": "Mexico", "code": "MX"}, {"region": "Moldova, Republic of Moldova", "code": "MD"}, {"region": "Monaco", "code": "MC"}, {"region": "Mongolia", "code": "MN"}, {"region": "Montenegro", "code": "ME"}, {"region": "Montserrat", "code": "MS"}, {"region": "Morocco", "code": "MA"}, {"region": "Mozambique", "code": "MZ"}, {"region": "Myanmar", "code": "MM"}, {"region": "Namibia", "code": "NA"}, {"region": "Nauru", "code": "NR"}, {"region": "Nepal", "code": "NP"}, {"region": "Netherlands", "code": "NL"}, {"region": "Netherlands Antilles", "code": "AN"}, {"region": "New Caledonia", "code": "NC"}, {"region": "New Zealand", "code": "NZ"}, {"region": "Nicaragua", "code": "NI"}, {"region": "Niger", "code": "NE"}, {"region": "Nigeria", "code": "NG"}, {"region": "Norfolk Island", "code": "NF"}, {"region": "North Korea", "code": "KP"}, {"region": "Northern Mariana Islands", "code": "MP"}, {"region": "Norway", "code": "NO"}, {"region": "Oman", "code": "OM"}, {"region": "Pakistan", "code": "PK"}, {"region": "Palau", "code": "PW"}, {"region": "Panama", "code": "PA"}, {"region": "Papua New Guinea", "code": "PG"}, {"region": "Paraguay", "code": "PY"}, {"region": "Peru", "code": "PE"}, {"region": "Philippines", "code": "PH"}, {"region": "Poland", "code": "PL"}, {"region": "Portugal", "code": "PT"}, {"region": "Qatar", "code": "QA"}, {"region": "Romania", "code": "RO"}, {"region": "Russian Federation", "code": "RU"}, {"region": "Rwanda", "code": "RW"}, {"region": "Saint Helena, Ascension, and Tristan da Cunha", "code": "SH"}, {"region": "Saint Kitts and Nevis", "code": "KN"}, {"region": "Samoa", "code": "WS"}, {"region": "San Marino", "code": "SM"}, {"region": "Sao Tome and Principe", "code": "ST"}, {"region": "Saudi Arabia", "code": "SA"}, {"region": "Senegal", "code": "SN"}, {"region": "Serbia", "code": "RS"}, {"region": "Seychelles", "code": "SC"}, {"region": "Sierra Leone", "code": "SL"}, {"region": "Singapore", "code": "SG"}, {"region": "Slovakia", "code": "SK"}, {"region": "Slovenia", "code": "SI"}, {"region": "Solomon Islands", "code": "SB"}, {"region": "Somalia", "code": "SO"}, {"region": "South Africa", "code": "ZA"}, {"region": "South Georgia and the South Sandwich Islands", "code": "GS"}, {"region": "South Korea", "code": "KR"}, {"region": "Spain", "code": "ES"}, {"region": "Sri Lanka", "code": "LK"}, {"region": "St. Lucia", "code": "LC"}, {"region": "St. Vincent and the Grenadines", "code": "VC"}, {"region": "Sudan", "code": "SD"}, {"region": "Suriname", "code": "SR"}, {"region": "Swaziland", "code": "SZ"}, {"region": "Sweden", "code": "SE"}, {"region": "Switzerland", "code": "CH"}, {"region": "Syria", "code": "SY"}, {"region": "Taiwan(Province of China)", "code": "TW"}, {"region": "Tajikistan", "code": "TJ"}, {"region": "Tanzania", "code": "TZ"}, {"region": "Thailand", "code": "TH"}, {"region": "Timor-Leste", "code": "TL"}, {"region": "Togo", "code": "TG"}, {"region": "Tonga", "code": "TO"}, {"region": "Trinidad and Tobago", "code": "TT"}, {"region": "Tunisia", "code": "TN"}, {"region": "Turkey", "code": "TR"}, {"region": "Turkmenistan", "code": "TM"}, {"region": "Turks and Caicos Islands", "code": "TC"}, {"region": "Tuvalu", "code": "TV"}, {"region": "Uganda", "code": "UG"}, {"region": "Ukraine", "code": "UA"}, {"region": "United Kingdom", "code": "GB"}, {"region": "United States of America", "code": "US"}, {"region": "Uruguay", "code": "UY"}, {"region": "Uzbekistan", "code": "UZ"}, {"region": "Vanuatu (New Hebrides)", "code": "VU"}, {"region": "Vatican City State (Holy See)", "code": "VA"}, {"region": "Venezuela", "code": "VE"}, {"region": "Viet Nam", "code": "VN"}, {"region": "Virgin (British) Islands", "code": "VG"}, {"region": "Western Sahara", "code": "EH"}, {"region": "Yemen", "code": "YE"}, {"region": "Yugoslavia", "code": "YU"}, {"region": "Zambia", "code": "ZM"}, {"region": "Zimbabwe", "code": "ZW"}]}']]
correct_response['currency_list/'][STATUS_CODE["success"]] = [["GET", "", '{"status": 0, "currency_list": [{"currency_type": "Australian Dollar", "code": "AUD"}, {"currency_type": "Brazilian Real", "code": "BRL"}, {"currency_type": "British Pound", "code": "GBP"}, {"currency_type": "Canadian Dollar", "code": "CAD"}, {"currency_type": "Chinese Yuan Renminbi", "code": "CNY"}, {"currency_type": "Czech Koruna", "code": "CZK"}, {"currency_type": "Danish Krone", "code": "DKK"}, {"currency_type": "Euro", "code": "EUR"}, {"currency_type": "Hong Kong Dollar", "code": "HKD"}, {"currency_type": "Hungarian Forint", "code": "HUF"}, {"currency_type": "Israeli Shekel", "code": "ILS"}, {"currency_type": "Japanese Yen", "code": "JPY"}, {"currency_type": "Malaysian Ringgit", "code": "MYR"}, {"currency_type": "Mexican Peso", "code": "MXN"}, {"currency_type": "New Zealand Dollar", "code": "NZD"}, {"currency_type": "Norwegian Krone", "code": "NOK"}, {"currency_type": "Philippine Peso", "code": "PHP"}, {"currency_type": "Polish Zloty", "code": "PLN"}, {"currency_type": "Russian Ruble", "code": "RUB"}, {"currency_type": "Singapore Dollar", "code": "SGD"}, {"currency_type": "Swedish Krona", "code": "SEK"}, {"currency_type": "Swiss Franc", "code": "CHF"}, {"currency_type": "Taiwan New Dollar", "code": "TWD"}, {"currency_type": "Thai Baht", "code": "THB"}, {"currency_type": "US Dollar", "code": "USD"}]}']]
correct_response['region2currency/'][STATUS_CODE["success"]] = [["GET", "", '{"status": 0, "region2currency": {"AE": "GBP", "AF": "GBP", "AL": "GBP", "AM": "GBP", "AN": "GBP", "CW": "GBP", "AO": "GBP", "AR": "GBP", "AU": "AUD", "CC": "AUD", "KI": "AUD", "NF": "AUD", "NR": "AUD", "TV": "AUD", "AW": "GBP", "BA": "GBP", "BB": "GBP", "BD": "GBP", "BG": "GBP", "BH": "GBP", "BI": "GBP", "BM": "GBP", "BN": "GBP", "BO": "GBP", "BR": "BRL", "BS": "GBP", "BT": "GBP", "BW": "GBP", "BY": "GBP", "BZ": "GBP", "CA": "CAD", "CD": "GBP", "CH": "CHF", "LI": "CHF", "CL": "GBP", "CN": "CNY", "CO": "GBP", "CR": "GBP", "RS": "GBP", "CU": "GBP", "CV": "GBP", "CY": "GBP", "CZ": "CZK", "DJ": "GBP", "DK": "DKK", "FO": "DKK", "GL": "DKK", "DO": "GBP", "DZ": "GBP", "EE": "GBP", "EG": "GBP", "ER": "GBP", "ET": "GBP", "AD": "EUR", "AT": "EUR", "BE": "EUR", "DE": "EUR", "ES": "EUR", "FI": "EUR", "FR": "EUR", "GF": "EUR", "GP": "EUR", "GR": "EUR", "IE": "EUR", "IT": "EUR", "LU": "EUR", "MC": "EUR", "ME": "EUR", "MQ": "EUR", "NL": "EUR", "PT": "EUR", "SM": "EUR", "VA": "EUR", "FJ": "GBP", "FK": "GBP", "AZ": "GBP", "GB": "GBP", "GG": "GBP", "GS": "GBP", "IM": "GBP", "JE": "GBP", "GE": "GBP", "GH": "GBP", "GI": "GBP", "GM": "GBP", "GN": "GBP", "GT": "GBP", "GY": "GBP", "HK": "HKD", "HN": "GBP", "HR": "GBP", "HT": "GBP", "HU": "HUF", "ID": "GBP", "IL": "ILS", "IN": "GBP", "IQ": "GBP", "IR": "GBP", "IS": "GBP", "JM": "GBP", "JO": "GBP", "JP": "JPY", "KE": "GBP", "KG": "GBP", "KH": "GBP", "KM": "GBP", "KP": "GBP", "KR": "GBP", "KW": "GBP", "KY": "GBP", "KZ": "GBP", "LA": "GBP", "LB": "GBP", "LK": "GBP", "LR": "GBP", "LS": "GBP", "LT": "GBP", "LV": "GBP", "LY": "GBP", "EH": "GBP", "MA": "GBP", "MD": "GBP", "MG": "GBP", "MK": "GBP", "MM": "GBP", "MN": "GBP", "MO": "GBP", "MR": "GBP", "MT": "GBP", "MU": "GBP", "MV": "GBP", "MW": "GBP", "MX": "MXN", "MY": "MYR", "MZ": "GBP", "NA": "GBP", "NG": "GBP", "NI": "GBP", "BV": "NOK", "NO": "NOK", "NP": "GBP", "CK": "NZD", "NZ": "NZD", "OM": "GBP", "PA": "GBP", "PE": "GBP", "PG": "GBP", "PH": "PHP", "PK": "GBP", "PL": "PLN", "PY": "GBP", "QA": "GBP", "RO": "GBP", "RU": "RUB", "RW": "GBP", "SA": "GBP", "SB": "GBP", "SC": "GBP", "SD": "GBP", "SE": "SEK", "SG": "SGD", "SH": "GBP", "SI": "GBP", "SK": "GBP", "SL": "GBP", "SO": "GBP", "SR": "GBP", "ST": "GBP", "SV": "GBP", "SY": "GBP", "SZ": "GBP", "TH": "THB", "TJ": "GBP", "TM": "GBP", "TN": "GBP", "TO": "GBP", "TL": "GBP", "TR": "GBP", "TT": "GBP", "TW": "TWD", "TZ": "GBP", "UA": "GBP", "UG": "GBP", "EC": "USD", "MH": "USD", "MP": "USD", "PW": "USD", "TC": "USD", "US": "USD", "VG": "USD", "UY": "GBP", "UZ": "GBP", "VE": "GBP", "VN": "GBP", "VU": "GBP", "WS": "GBP", "CF": "GBP", "CG": "GBP", "CM": "GBP", "GA": "GBP", "GQ": "GBP", "TD": "GBP", "AG": "GBP", "AI": "GBP", "DM": "GBP", "GD": "GBP", "KN": "GBP", "LC": "GBP", "MS": "GBP", "VC": "GBP", "BF": "GBP", "BJ": "GBP", "CI": "GBP", "GW": "GBP", "ML": "GBP", "NE": "GBP", "SN": "GBP", "TG": "GBP", "NC": "GBP", "PF": "GBP", "YE": "GBP", "YU": "GBP", "ZA": "GBP", "ZM": "GBP", "ZW": "GBP"}}']]

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
            r = rs.post(url_dict[api], headers=headers, files={key: f, 'Content-Type': 'multipart/form-data'})
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
                        user["password"] = i["password"]
                        break

                f.write(check_api('login/', STATUS_CODE["invalid username"], "POST", {"username": "test" + user["mail"], "password": user["password"]}, '{"status": %d}' % STATUS_CODE["invalid username"]) + "\n")
                f.write(check_api('login/', STATUS_CODE["wrong password"], "POST", {"username": user["mail"], "password": "test" + user["password"]}, '{"status": %d}' % STATUS_CODE["wrong password"]) + "\n")
                f.write(check_api('login/', STATUS_CODE["success"], "POST", {"username": user["mail"], "password": user["password"]}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('login/', STATUS_CODE["user is already logged in"], "POST", {"username": user["mail"], "password": user["password"]}, '{"status": %d}' % STATUS_CODE["user is already logged in"]) + "\n")

                f.write(check_api('logout/', STATUS_CODE["success"], "GET", "", '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('logout/', STATUS_CODE["user is not logged in"], "GET", "", '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")

                f.write(check_api('regis/', STATUS_CODE["invalid action"], "POST", {"username": user["mail"], "action": 4}, '{"status": %d, "action": 4}' % STATUS_CODE["invalid action"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["email is already registered"], "POST", {"username": user["mail"], "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["email is already registered"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["email delivery failed"], "POST", {"username": "test", "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["email delivery failed"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["success"], "POST", {"username": mail, "action": 0}, '{"status": %d, "action": 0}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["captcha verification failed"], "POST", {"username": mail, "action": 1, "code": "testtest"}, '{"status": %d, "action": 1}' % STATUS_CODE["captcha verification failed"]) + "\n")
                #code = gen_verify_code(mail, "regis")
                code = input("Input registration verification code: ")
                f.write(check_api('regis/', STATUS_CODE["success"], "POST", {"username": mail, "action": 1, "code": code}, '{"status": %d, "action": 1}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["wrong parameters for user creation"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "CN", "currency_type": "GBP", "name": "tyl", "avatar": ""}, '{"status": %d, "action": 2}' % STATUS_CODE["wrong parameters for user creation"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["invalid user type"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "CN", "currency_type": "GBP", "name": "tyl", "avatar": "", "type": 9}, '{"status": %d, "action": 2}' % STATUS_CODE["invalid user type"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["wrong region name or code"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "testCN", "currency_type": "GBP", "name": "tyl", "avatar": "", "type": 2}, '{"status": %d, "action": 2}' % STATUS_CODE["wrong region name or code"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["invalid currency type"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "CN", "currency_type": "testGBP", "name": "tyl", "avatar": "", "type": 2}, '{"status": %d, "action": 2}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('regis/', STATUS_CODE["success"], "POST", {"username": mail, "action": 2, "code": code, "password": password, "region": "CN", "currency_type": "GBP", "name": "tyl", "avatar": "", "type": 2}, '{"status": %d, "action": 2}' % STATUS_CODE["success"]) + "\n")
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

                f.write(check_api('get_user/', STATUS_CODE["user is not logged in"], "GET", "", '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")
                user_login(user["mail"], user["password"])
                f.write(check_api('get_user/', STATUS_CODE["success"], "GET", "", '{"status": %d, "user_info": {"uid": "%s", "mail": "%s", .*}' % (STATUS_CODE["success"], user["uid"], user["mail"])) + "\n")

                f.write(check_api('edit_user/', STATUS_CODE["invalid currency type"], "POST", {"name": "test", "region": "Afghanistan", "currency_type": "testUSD", "avatar": ""}, '{"status": %d}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('edit_user/', STATUS_CODE["wrong region name or code"], "POST", {"name": "test", "region": "testAfghanistan", "currency_type": "USD", "avatar": ""}, '{"status": %d}' % STATUS_CODE["wrong region name or code"]) + "\n")
                f.write(check_api('edit_user/', STATUS_CODE["success"], "POST", {"name": "test", "region": "Afghanistan", "currency_type": "USD", "avatar": ""}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                user_logout()
                f.write(check_api('edit_user/', STATUS_CODE["user is not logged in"], "POST", {"name": "test", "region": "Afghanistan", "currency_type": "USD", "avatar": ""}, '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")
                #100002 can't be test

                f.write(check_api('create_project/', STATUS_CODE["user is not logged in"], "GET", "", '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")
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
                f.write(check_api('edit_project/', STATUS_CODE["user is not logged in"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) - 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('edit_project/', STATUS_CODE["user is not the owner of the project"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) - 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["user is not the owner of the project"]) + "\n")
                #200005 can't be test

                f.write(check_api('start_project/', STATUS_CODE["user is not the owner of the project"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not the owner of the project"]) + "\n")
                user_logout()
                f.write(check_api('start_project/', STATUS_CODE["user is not logged in"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")
                user_login(user["mail"], user["password"])
                f.write(check_api('start_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"]}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                f.write(check_api('start_project/', STATUS_CODE["project information is incomplete"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project information is incomplete"]) + "\n")
                f.write(check_api('edit_project/', STATUS_CODE["project price invalid"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) + 24 * 60 * 60, "details": "apex", "price": -100}}, '{"status": %d}' % STATUS_CODE["project price invalid"]) + "\n")
                f.write(check_api('edit_project/', STATUS_CODE["success"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) + 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('start_project/', STATUS_CODE["success"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('edit_project/', STATUS_CODE["project is not editable"], "POST", {"pid": project["pid"], "currency_type": "CNY", "edit": {"title": "apex", "intro": "apex", "background_image": "", "total_num": 80, "end_time": int(time.time()) - 24 * 60 * 60, "details": "apex", "price": 100}}, '{"status": %d}' % STATUS_CODE["project is not editable"]) + "\n")
                f.write(check_api('start_project/', STATUS_CODE["project has already started"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project has already started"]) + "\n")
                #200008 can't be test

                f.write(check_api('stop_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"]}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                user_logout()
                f.write(check_api('stop_project/', STATUS_CODE["user is not logged in"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('stop_project/', STATUS_CODE["user is not the owner of the project"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not the owner of the project"]) + "\n")
                user_logout()
                user_login(user["mail"], user["password"])
                f.write(check_api('stop_project/', STATUS_CODE["success"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["success"]) + "\n")
                f.write(check_api('stop_project/', STATUS_CODE["project is not ongoing"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project is not ongoing"]) + "\n")
                #200010 can't be test

                f.write(check_api('delete_project/', STATUS_CODE["project does not exist"], "POST", {"pid": "test" + project["pid"]}, '{"status": %d}' % STATUS_CODE["project does not exist"]) + "\n")
                f.write(check_api('delete_project/', STATUS_CODE["project is not deletable"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["project is not deletable"]) + "\n")
                user_logout()
                f.write(check_api('delete_project/', STATUS_CODE["user is not logged in"], "POST", {"pid": project["pid"]}, '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")
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
                f.write(check_api('get_prepare_projects_list/', STATUS_CODE["user is not logged in"], "POST", {"currency_type": "CNY", "page_info": {"page_size": 3, "page": 1}, "search": "q"}, '{"status": %d}' % STATUS_CODE["user is not logged in"]) + "\n")
                user_login(mail, reset_password)
                f.write(check_api('get_prepare_projects_list/', STATUS_CODE["operation is not available to individual user"], "POST", {"currency_type": "CNY", "page_info": {"page_size": 3, "page": 1}, "search": "q"}, '{"status": %d}' % STATUS_CODE["operation is not available to individual user"]) + "\n")

                f.write(check_api('get_projects_list/', STATUS_CODE["project order invalid"], "POST", {"order": "-testprogress", "currency_type": "CNY", "page_info": {"page_size": 5, "page": 1}, "search": "", "valid_only": 1, "uid": ""}, '{"status": %d}' % STATUS_CODE["project order invalid"]) + "\n")
                f.write(check_api('get_projects_list/', STATUS_CODE["invalid currency type"], "POST", {"order": "-progress", "currency_type": "testCNY", "page_info": {"page_size": 5, "page": 1}, "search": "", "valid_only": 1, "uid": ""}, '{"status": %d}' % STATUS_CODE["invalid currency type"]) + "\n")
                f.write(check_api('get_projects_list/', STATUS_CODE["success"], "POST", {"order": "-progress", "currency_type": "CNY", "page_info": {"page_size": 5, "page": 1}, "search": "", "valid_only": 1, "uid": ""}, '{"status": %d.*}' % STATUS_CODE["success"]) + "\n")

                for _ in range(10):
                    user_login("test", "test")
                f.write(check_api('login/', STATUS_CODE["temporary ban due to too frequent login attempts"], "POST", {"username": "test" + user["mail"], "password": user["password"]}, '{"status": %d}' % STATUS_CODE["temporary ban due to too frequent login attempts"]) + "\n")
                