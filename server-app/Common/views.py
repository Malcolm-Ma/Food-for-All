import json
from django.http import HttpResponse
from FoodForAll.settings import REGION2RID, RID2REGION

# Create your views here.
def get_region(request):
    sep = "#"
    response_data = {"region_list": sep.join(list(REGION2RID.keys())),
                     "split": sep}
    return HttpResponse(json.dumps(response_data), content_type="application/json")