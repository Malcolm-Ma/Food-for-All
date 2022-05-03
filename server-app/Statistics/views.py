from .functions import Statistics
from Common.decorators import *


def get_report(request):
    data = json.loads(request.body)
    id_ = data['id']
    id_type = data['type']
    
    file_name = Statistics.generate_report(id_, id_type)
    response_data = {'status': STATUS_CODE['success'], "url": os.path.join(STATIC_URL, file_name)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')
