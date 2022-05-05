from .functions import Statistics
from Common.decorators import *


def get_stat(request):
    data = json.loads(request.body)
    id_ = data['id']
    type_ = data['type']

    d = Statistics.get_project_dict(id_) if type_ == 'project' else Statistics.get_user_dict(id_)
    overall_sum, monthly_sum = Statistics.get_donation_sum(d)
    progress = Statistics.get_progress(d)
    region_dist = Statistics.get_region_distribution(d)
    stat = {'overall_sum': overall_sum,
            'monthly_sum': dict(zip(monthly_sum[0], monthly_sum[1])),
            'progress': dict(zip(progress[0], progress[1])) if type_ == 'project' else 0,
            'region_dist': dict(zip(region_dist[0], region_dist[1]))}
    response_data = {'status': STATUS_CODE['success'], 'stat': stat}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def get_report(request):
    data = json.loads(request.body)
    id_ = data['id']
    type_ = data['type']

    file_name = Statistics.get_project_report(id_) if type_ == 'project' else Statistics.get_user_report(id_)
    response_data = {'status': STATUS_CODE['success'], 'url': file_name}  # Reshape url when merge into main
    return HttpResponse(json.dumps(response_data), content_type='application/json')
