from User.functions import *

login_status = {"success": 0,
                "already_login": 1,
                "wrong_username": 2,
                "wrong_password": 3,}

regis_status = {"mail_registered": 0,
                "already_login": 1,
                "mail_send_success": 2,
                "mail_send_fail": 3,
                "code_verify_success": 4,
                "code_verify_fail": 5,
                "set_password_success": 6,
                "set_password_fail": 7,
                "wrong_action": 8}

regis_action = {"send_code": 0,
                "verify_code": 1,
                "set_password": 2}

logout_status = {"success": 0,
                 "not_logged_in": 1}

reset_password_status = {"mail_not_registered": 0,
                         "user_not_match": 1,
                         "mail_send_success": 2,
                         "mail_send_fail": 3,
                         "code_verify_success": 4,
                         "code_verify_fail": 5,
                         "set_password_success": 6,
                         "set_password_fail": 7,
                         "wrong_action": 8}

reset_password_action = {"send_code": 0,
                         "verify_code": 1,
                         "set_password": 2}