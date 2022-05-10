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
            "date": ["2022/03/21", "2022/03/22", "2022/03/23", "2022/03/24", "2022/03/25", "2022/03/26", "2022/03/27", "2022/03/28", "2022/03/29", "2022/03/30", "2022/03/31", "2022/04/01", "2022/04/02", "2022/04/03", "2022/04/04", "2022/04/05", "2022/04/06", "2022/04/07", "2022/04/08", "2022/04/09", "2022/04/10", "2022/04/11", "2022/04/12", "2022/04/13", "2022/04/14", "2022/04/15", "2022/04/16", "2022/04/17", "2022/04/18", "2022/04/19", "2022/04/20", "2022/04/21", "2022/04/22", "2022/04/23", "2022/04/24", "2022/04/25", "2022/04/26", "2022/04/27", "2022/04/28", "2022/04/29", "2022/04/30", "2022/05/01", "2022/05/02", "2022/05/03", "2022/05/04", "2022/05/05", "2022/05/06", "2022/05/07", "2022/05/08", "2022/05/09"],
            "title": ["Children\u2019s food insecurity increasing during COVID-19 pandemic_3ae42f26", "Life-saving food in emergencies_a492468d"],
            "pie": [{"value": "79.24", "name": "Barbados"}, {"value": "56.80", "name": "China, Hong Kong S.A.R."}, {"value": "51.71", "name": "Estonia"}, {"value": "50.68", "name": "Mauritania"}, {"value": "50.21", "name": "Spain"}, {"value": "49.74", "name": "Poland"}, {"value": "49.51", "name": "Niger"}, {"value": "48.25", "name": "Comoros"}, {"value": "503.92", "name": "Others"}],
            "progress": [{"name": "Children\u2019s food insecurity increasing during COVID-19 pandemic_3ae42f26", "type": "line", "data": ["", "1.54", "5.38", "10.00", "16.15", "16.15", "18.46", "23.85", "26.92", "30.77", "34.62", "35.38", "38.46", "40.77", "44.62", "44.62", "44.62", "47.69", "50.00", "50.00", "53.08", "54.62", "54.62", "57.69", "57.69", "66.92", "66.92", "70.00", "70.77", "71.54", "76.92", "77.69", "77.69", "77.69", "80.77", "81.54", "81.54", "81.54", "82.31", "82.31", "82.31", "83.08", "83.08", "85.38", "92.31", "93.85", "93.85", "96.92", "96.92", 100]}, {"name": "Life-saving food in emergencies_a492468d", "type": "line", "data": ["", "", "", "", "", "", "", "", "", "", "", "", "", "1.03", "4.14", "8.97", "12.76", "19.66", "24.48", "32.07", "36.21", "37.93", "44.83", "48.97", "51.03", "55.17", "56.55", "59.66", "61.03", "65.86", "67.59", "72.07", "74.14", "75.86", "77.24", "78.62", "80.00", "82.41", "83.10", "84.48", "86.55", "86.55", "87.24", "94.48", "94.83", "96.55", "97.93", "97.93", "97.93", "97.93"]}],
            "history": [{"name": "Children\u2019s food insecurity increasing during COVID-19 pandemic_3ae42f26", "type": "bar", "stack": "total", "label": {"show": "true"}, "emphasis": {"focus": "series"}, "data": ["", "4.86", "12.15", "14.59", "19.45", "", "7.29", "17.02", "9.72", "12.15", "12.15", "2.43", "9.72", "7.29", "12.15", "", "", "9.72", "7.29", "", "9.72", "4.86", "", "9.72", "", "29.17", "", "9.72", "2.43", "2.43", "17.02", "2.43", "", "", "9.72", "2.43", "", "", "2.43", "", "", "2.43", "", "7.29", "21.88", "4.86", "", "9.72", "", "9.72"]}, {"name": "Life-saving food in emergencies_a492468d", "type": "bar", "stack": "total", "label": {"show": "true"}, "emphasis": {"focus": "series"}, "data": ["", "", "", "", "", "", "", "", "", "", "", "", "", "6.59", "19.78", "30.76", "24.17", "43.94", "30.76", "48.34", "26.37", "10.99", "43.94", "26.37", "13.18", "26.37", "8.79", "19.78", "8.79", "30.76", "10.99", "28.56", "13.18", "10.99", "8.79", "8.79", "8.79", "15.38", "4.39", "8.79", "13.18", "", "4.39", "46.14", "2.20", "10.99", "8.79", "", "", ""]}]}}
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
