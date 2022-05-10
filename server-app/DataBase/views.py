from .functions import *
from Common.decorators import *

@check_request_method_decorator(method=["GET"])
def init_database(request):
    if not DEBUG:
        return HttpResponse(json.dumps({"Info": "The current environment is not a debug environment, so this interface is not valid. Please call this interface after restarting the service in a debug environment."}), content_type="application/json")
    if request.method == "GET":
        user_num = 50
        project_num = 100
    #elif request.method == "POST":
    #    data = json.loads(request.body)
    #    user_num = data["user_num"]
    #    project_num = data["project_num"]
    else:
        return HttpResponseBadRequest()
    user_list = init_database_with_fake_data(user_num, project_num)
    with open(os.path.join(BASE_DIR, "../demo/test_backend_api", "init_database_user.csv"), 'w', newline='') as f:
        writer = csv.writer(f)
        for row in user_list:
            writer.writerow(row)
    return HttpResponse(json.dumps({"user_num": user_num, "project_num": project_num, "user_list": user_list[1:]}), content_type="application/json")