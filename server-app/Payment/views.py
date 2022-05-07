from Common.decorators import *

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@get_project_decorator()
def pay(request, project):
    """
    @api {POST} /pay/ pay
    @apiVersion 1.0.0
    @apiName pay
    @apiGroup Payment
    @apiDescription api to pay for a project

    @apiParam {String} pid Pid of the project.
    @apiParam {Int} num Number of donations.
    @apiParam {String} currency_type Currency type.
    @apiParam {Int} plan Confirm if it is a recurring payment plan.(0: not pan, 1: plan)
    @apiParam {String} return_url The url to redirect to after the payment has approved.(Note that it must start with http:// or https://).
    @apiParam {String} cancel_url The url to redirect to after the payment has cancelled.(Note that it must start with http:// or https://).

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [200002] project does not exist)
    @apiSuccess (Success 200 return) {String} payment_id Payment ID.
    @apiSuccess (Success 200 return) {String} payment_url Payment Link.

    @apiParamExample {Json} Sample Request
    {
        "pid": "22fd90badc08090a9b01606dbee18ff1",
        "num": 2,
        "currency_type": "GBP",
        "plan": 0,
        "return_url": "http://www.baidu.com",
        "cancel_url": "http://www.google.com"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "payment_id": "0KX90338MR762615F",
        "payment_url": "https://www.sandbox.paypal.com/checkoutnow?token=0KX90338MR762615F"
    }
    """
    response_data = {"status": STATUS_CODE["success"], "payment_id": "", "payment_url": ""}
    data = json.loads(request.body)
    num = data["num"]
    currency_type = data["currency_type"]
    as_plan = data["plan"]
    return_url = data["return_url"]
    cancel_url = data["cancel_url"]
    project_info = project.to_dict(currency_type=currency_type)
    price = num * project_info["price"]
    if as_plan:
        create_plan = Payment.create_plan(project.product_id, (str(int(time.time())) + "_" + project.title)[:127], "{price} {currency_type} per month pay for project {name} for 12 months".format(price=str(price), currency_type=currency_type, name=project.title), currency_type, price)
        create_subscription = Payment.create_subscription(create_plan["id"], (str(int(time.time())) + "_" + project.title)[:127], return_url, cancel_url)
        response_data["payment_id"] = create_subscription["id"]
        response_data["payment_url"] = [i for i in create_subscription["links"] if i["rel"] == "approve"][0]["href"]
    else:
        create_order = Payment.create_order(currency_type, price, return_url, cancel_url)
        response_data["payment_id"] = create_order["id"]
        response_data["payment_url"] = [i for i in create_order["links"] if i["rel"] == "approve"][0]["href"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@get_user_decorator(force_login=False)
@get_project_decorator()
def capture_payment(request, user, project):
    """
    @api {POST} /capture_payment/ capture_payment
    @apiVersion 1.0.0
    @apiName capture_payment
    @apiGroup Payment
    @apiDescription api to capture a payment

    @apiParam {String} pid Pid of the project.
    @apiParam {Int} num Number of donations.
    @apiParam {String} payment_id Payment ID.
    @apiParam {Int} plan Confirm if it is a recurring payment plan.(0: not pan, 1: plan)

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [500002] payment capture failed)

    @apiParamExample {Json} Sample Request
    {
        "pid": "22fd90badc08090a9b01606dbee18ff1",
        "num": 2,
        "payment_id": "0KX90338MR762615F",
        "plan": 0
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    data = json.loads(request.body)
    num = data["num"]
    payment_id = data["payment_id"]
    as_plan = data["plan"]
    if as_plan:
        show_subscription = Payment.show_subscription(payment_id)
        if "status" not in show_subscription or show_subscription["status"] != "ACTIVE":
            raise ServerError("payment capture failed")
    else:
        capture_order = Payment.capture_order(payment_id)
        if "id" not in capture_order or capture_order["status"] != "COMPLETED":
            raise ServerError("payment capture failed")
    donate_time = str(int(time.time()))
    if not user:
        uid = "Anonymous"
    else:
        uid = user.uid
        user_project = eval(user.project)
        if project.pid not in user_project:
            user_project.append(project.pid)
            user.project = str(user_project)
            user.save(update_fields=["project"])
            user_donate_history = eval(user.donate_history)
            user_donate_history[project.pid] = dict()
        user_donate_history[project.pid][donate_time] = num
        user.donate_history = str(user_donate_history)
        user.save(update_fields=["donate_history"])
    project_donate_history = eval(project.donate_history)
    if uid not in project_donate_history:
        project_donate_history[uid] = dict()
    project_donate_history[uid][donate_time] = num
    project.donate_history = str(project_donate_history)
    project.save(update_fields=["donate_history"])
    if as_plan:
        if project.subscription_list == "":
            project_subscription_list = []
        else:
            project_subscription_list = eval(project.subscription_list)
        project_subscription_list.append(payment_id)
        project.subscription_list = str(project_subscription_list)
        project.save(update_fields=["subscription_list"])
    project_owner = DUser.get_user({"uid": project.uid})
    project_owner_donate_history = eval(project_owner.donate_history)
    if project.pid not in project_owner_donate_history:
        project_owner_donate_history[project.pid] = dict()
    if uid not in project_owner_donate_history[project.pid]:
        project_owner_donate_history[project.pid][uid] = dict()
    project_owner_donate_history[project.pid][uid][donate_time] = num
    project_owner.donate_history = str(project_owner_donate_history)
    project_owner.save(update_fields=["donate_history"])
    return HttpResponse(json.dumps(response_data), content_type="application/json")