from Common.common import *
from Common.utils import *
from Common.decorators import *

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@get_user_decorator(force_login=False)
def share_by_email(request, user):
    """
    @api {POST} /share_by_email/ share by email
    @apiVersion 1.0.0
    @apiName share_by_email
    @apiGroup Common
    @apiDescription api to share by email after donation

    @apiParam {List(String)} mail List of email addresses to share to.
    @apiParam {String} project_name Name of the project that have just been donated.
    @apiParam {String} project_url Website url of the project that have just been donated.
    @apiParam {Int} donate_num Number of meals that have just been donated.
    @apiParam {Int} if_hide_personal_information Whether the user is hiding personal information in share email or not. (0: no hide, 1: hide)
    @apiParam {String} user_name Name of the donor. If user has logged in, this field could be populated with "".

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success)

    @apiParamExample {Json} Sample Request
    {
        "mail": ["qwer@gmail.com", "asdf@gmail.com"],
        "project_name": "Test project",
        "project_url": "http://127.0.0.1:3000/project/qwerasdf/",
        "donate_num": 2,
        "if_hide_personal_information": 0,
        "user_name": "Richard"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    data = json.loads(request.body)
    share_info = {}
    share_info["mail"] = data["mail"]
    share_info["project_name"] = data["project_name"]
    share_info["project_url"] = data["project_url"]
    share_info["donate_num"] = data["donate_num"]
    if_hide_personal_information = data["if_hide_personal_information"]
    if user:
        update_dict = {"share_mail_history": share_info["mail"]}
        share_info["user_name"] = user.name
        try:
            user.update_from_fict(update_dict)
        except ServerError as se:
            logger_standard.error("User {uid} update share_mail_history failed.".format(uid=user.uid))
    else:
        share_info["user_name"] = data["user_name"]
    if if_hide_personal_information:
        share_info["user_name"] = ""
    try:
        Mail.share(share_info, False)
    except:
        logger_standard.warning("Send share mail to {mail} failed.".format(mail=str(share_info["mail"])))
    return HttpResponse(json.dumps(response_data), content_type="application/json")
