from .functions import Statistics
from Common.decorators import *


def get_report(request):
    data = json.loads(request.body)
    id_ = data['id']
    type_ = data['type']

    file_name = Statistics.get_project_report(id_) if type_ == 'project' else Statistics.get_user_report(id_)
    response_data = {'status': STATUS_CODE['success'], "url": os.path.join(STATIC_URL, file_name)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')
