from .functions import Statistics
from Common.decorators import *


@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@get_user_decorator()
def get_stat(request, user):
    """
    @api {POST} /get_stat/ get statistics data
    @apiVersion 1.0.0
    @apiName get_stat
    @apiGroup Statistics
    @apiDescription Get statistics data for frontend dashboard

    @apiParam {String} pid Leave blank to get data of the current user or specify a pid of any affiliated project.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project)
    @apiSuccess (Success 200 return) {Dict} stat Statistics data.
    @apiSuccess (Success 200 return) {List(String)} date (Sub-parameter of stat) Time line of donation.
    @apiSuccess (Success 200 return) {List(String)} title (Sub-parameter of stat) Project name of donation.
    @apiSuccess (Success 200 return) {List(Dict)} pie (Sub-parameter of stat) Progress data of donation.
    @apiSuccess (Success 200 return) {List(Dict)} progress (Sub-parameter of stat) Progress of donation.
    @apiSuccess (Success 200 return) {List(Dict)} history (Sub-parameter of stat) History of donation.

    @apiParamExample {Json} Sample Request
    {
      "pid": ""
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "stat": {
            "date": ["2022/03/21", "2022/03/22", "2022/03/23", ...,
            "title": ["Children\u2019s food insecurity increasing during COVID-19 pandemic_3ae42f26", "Life-saving food in emergencies_a492468d"],
            "pie": [{"value": "79.24", "name": "Barbados"}, {"value": "56.80", "name": "China, Hong Kong S.A.R."}, ...,
            "progress": [{"name": "Children\u2019s food insecurity increasing during COVID-19 pandemic_3ae42f26", "type": "line", "data": ["", "1.54", "5.38", "10.00", ...,
            "history": [{"name": "Children\u2019s food insecurity increasing during COVID-19 pandemic_3ae42f26", "type": "bar", "stack": "total", "label": {"show": "true"}, "emphasis": {"focus": "series"}, "data": ["", "4.86", "12.15", "14.59", ...
        }
    }
    """
    data = json.loads(request.body)
    pid = data['pid']
    if pid:
        project = DProject.get_project({'pid': pid})
        if not project:
            raise ServerError("project does not exist")
        if user.uid != project.uid:
            raise ServerError("user is not the owner of the project")
        d = Statistics.get_project_dict(pid)
    else:
        d = Statistics.get_user_dict(user.uid)
    # progress = Statistics.get_progress(d) if pid else {}
    time_line = Statistics.get_time_line(d)
    regional_dist = Statistics.m_get_regional_dist(d)
    project_name = Statistics.get_project_name(d)
    progress = Statistics.get_monthly_progress(d)

    progress_data = []
    if len(regional_dist[0]) < 8:
        for name, value in zip(regional_dist[0], regional_dist[1]):
            progress_data.append({'value': "%.2f" % value, 'name': name})
    else:
        i = 0;
        other_value = 0
        for name, value in zip(regional_dist[0], regional_dist[1]):
            if i < 8:
                progress_data.append({'value': "%.2f" % value, 'name': name})
                i += 1
            else:
                other_value += value
        progress_data.append({'value': "%.2f" % other_value, 'name': 'Others'})

    stat = {
        'date': time_line,
        'title': project_name,
        'pie': progress_data,
        'progress': progress,
        'history': Statistics.get_history(d)
    }

    response_data = {'status': STATUS_CODE['success'], 'stat': stat}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@get_user_decorator()
def get_report(request, user):
    """
    @api {POST} /get_report/ get statistics pdf report
    @apiVersion 1.0.0
    @apiName get_report
    @apiGroup Statistics
    @apiDescription api to get statistics pdf report

    @apiParam {String} pid Leave blank to get report of the current user or specify a pid of any affiliated project.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project)
    @apiSuccess (Success 200 return) {String} url URL of report.

    @apiParamExample {Json} Sample Request
    {
      "pid": "adfasdfasdfasdsf"
    }
    @apiSuccessExample {Json} Response-Success
    {
        'status': 0
        "url": "static/p_adfasdfasdfasdsf.pdf"
    }
    """
    data = json.loads(request.body)
    pid = data['pid']
    if pid:
        project = DProject.get_project({'pid': pid})
        if not project:
            raise ServerError("project does not exist")
        if user.uid != project.uid:
            raise ServerError("user is not the owner of the project")
        filename = Statistics.get_project_report(pid)
    else:
        filename = Statistics.get_user_report(user.uid)
    response_data = {'status': STATUS_CODE['success'], 'url': os.path.join(STATIC_URL, filename)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')
