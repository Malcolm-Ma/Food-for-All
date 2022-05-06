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
    @apiDescription api to get statistics data for frontend dashboard

    @apiParam {String} pid Pid of the project (If get user's statistics data, just pass pid as "").

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project)
    @apiSuccess (Success 200 return) {Dict} stat Statistics information.
    @apiSuccess (Success 200 return) {Int} overall_sum Total sum of donation that charity receives.
    @apiSuccess (Success 200 return) {Dict} monthly_sum Monthly sum of donation. e.g. key: '202205', value: 100
    @apiSuccess (Success 200 return) {Dict} progress Statistics information. Monthly progress of a project. e.g. key: '202205', value: 0.5
    @apiSuccess (Success 200 return) {Dict} regional_dist Statistics information. Regional distribution of donation. e.g. key: 'China', value: 0.1

    @apiParamExample {Json} Sample Request
    {
      "pid": ""
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "stat": {
            "overall_sum": 2325.8058573595813,
            "monthly_sum": {
                "202110": 25.38635395622341,
                "202111": 83.94399337200952,
                "202112": 174.35017007224477,
                "202201": 269.812925171546,
                "202202": 560.2525941802537,
                "202203": 663.5475702441728,
                "202204": 259.78657985690444,
                "202205": 145.51878109829747
            },
            "progress": {},
            "regional_dist": {
                "": 0.1595509712334177,
                "Moldova, Republic of Moldova": 0.089812277796986,
                "Latvia": 0.05986185261846537,
                "Sri Lanka": 0.05946180316420208,
                "Dominica": 0.04336329633300498,
                "Spain": 0.03903952285678018,
                "Kiribati": 0.03757099035058154,
                "Madagascar": 0.03747727290665375,
                "Tonga": 0.036527191556695385,
                "Papua New Guinea": 0.035626688941039514,
                "Maldives": 0.03552259256316131,
                "Turkmenistan": 0.03519085713041302,
                "Denmark": 0.03493706048536908,
                "Antigua and Barbuda": 0.03418927440330687,
                "South Korea": 0.03195128590088027,
                "Hungary": 0.03193212530391174,
                "Palau": 0.02900629702106567,
                "Saint Helena, Ascension, and Tristan da Cunha": 0.028371282169266574,
                "Switzerland": 0.02687954360632756,
                "Montserrat": 0.024853387741580555,
                "Virgin (British) Islands": 0.023592879304021815,
                "Kazakhstan": 0.023318368481816006,
                "St. Lucia": 0.021326717636390324,
                "Jamaica": 0.020636460494662803
            }
        }
    }
    """
    data = json.loads(request.body)
    pid = data['pid']
    if pid == "":
        d = Statistics.get_user_dict(user.uid)
    else:
        project = DProject.get_project({"pid": pid})
        if not project:
            raise ServerError("project does not exist")
        if user.uid != project.uid:
            raise ServerError("user is not the owner of the project")
        d = Statistics.get_project_dict(pid)
    overall_sum, monthly_sum = Statistics.get_monthly_sum(d)
    if pid:
        progress = Statistics.get_progress(d)
    regional_dist = Statistics.get_regional_dist(d)
    stat = {'overall_sum': overall_sum,
            'monthly_sum': dict(zip(monthly_sum[0], monthly_sum[1])),
            'progress': dict(zip(progress[0], progress[1])) if pid else dict(),
            'regional_dist': dict(zip(regional_dist[0], regional_dist[1]))}
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

    @apiParam {String} pid Pid of the project (If get user's pdf report, just pass pid as "").

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project)
    @apiSuccess (Success 200 return) {String} url PDF report url.

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
    if pid == "":
        filename = Statistics.get_user_report(user.uid)
    else:
        project = DProject.get_project({"pid": pid})
        if not project:
            raise ServerError("project does not exist")
        if user.uid != project.uid:
            raise ServerError("user is not the owner of the project")
        filename = Statistics.get_project_report(pid)
    response_data = {'status': STATUS_CODE['success'], 'url': STATIC_URL + filename}  # Reshape url when merge into main
    return HttpResponse(json.dumps(response_data), content_type='application/json')
