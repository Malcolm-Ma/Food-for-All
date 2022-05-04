from .functions import Statistics
from Common.decorators import *


def get_stat(request):
    data = json.loads(request.body)
    id_ = data['id']
    type_ = data['type']

    d = Statistics.get_project_dict(id_) if type_ == 'project' else Statistics.get_user_dict(id_)
    overall_sum, monthly_sum = Statistics.get_donation_sum(d)
    monthly_sum = Statistics.transform_data(monthly_sum)
    completeness = Statistics.transform_data(Statistics.get_progress(d)) if type_ == 'project' else 0
    region_dist = Statistics.transform_data(Statistics.get_region_distribution(d))
    stat = {'overall_sum': overall_sum,
            'monthly_sum': monthly_sum,
            'completeness': completeness,
            'region_dist': region_dist}
    response_data = {'status': STATUS_CODE['success'], 'stat': stat}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def get_report(request):
    data = json.loads(request.body)
    id_ = data['id']
    type_ = data['type']

    file_name = Statistics.get_project_report(id_) if type_ == 'project' else Statistics.get_user_report(id_)
    response_data = {'status': STATUS_CODE['success'], 'url': os.path.join(STATIC_URL, file_name)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')
