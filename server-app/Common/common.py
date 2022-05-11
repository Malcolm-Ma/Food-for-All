from .functions import *
from .models import *
import logging

# The code of this script contains definitions of some generic parameters that are dependencies of most of the project code

# Setting the log level
logger_standard = logging.getLogger('standard')

# Some settings regarding cookies
COOKIE_KEY = "apex"
COOKIE_EXPIRES = 7 * 24 * 60 * 60
COOKIE_PATH = "/"
COOKIE_SALT = "apex"
COOKIE_ENCODE_KEY = 85

# Some settings for encrypting passwords
PASSWORD_ENCODE_KEY = 85

# Initialising the list of countries and the list of currency types
REGION2RID, RID2REGION = create_region_list()
CURRENCY2CID, CID2CURRENCY = create_currency_list()
RID2CID = create_region_currency_list()
EXCHANGE_RATE = create_exchange_rate()
REGION2CURRENCY = dict([[RID2REGION[i], CID2CURRENCY[j]] for i,j in RID2CID.items()])

# Define some conversion functions for currency codes and country codes
def region2rid(region):
    if region in REGION2RID:
        return REGION2RID[region]
    elif region in RID2REGION:
        return region
    else:
        return ""

def rid2region(rid):
    if rid in RID2REGION:
        return RID2REGION[rid]
    elif rid in REGION2RID:
        return rid
    else:
        return ""

def currency2cid(currency):
    if currency in CURRENCY2CID:
        return CURRENCY2CID[currency]
    elif currency in CID2CURRENCY:
        return currency
    else:
        return ""

def cid2currency(cid):
    if cid in CID2CURRENCY:
        return CID2CURRENCY[cid]
    elif cid in CURRENCY2CID:
        return cid
    else:
        return ""

# Function to get the ip address of request
def get_request_url(request):
    url = request.META.get('HTTP_X_FORWARDED_FOR')
    if not url:
        url = request.META.get('REMOTE_ADDR')
    return url