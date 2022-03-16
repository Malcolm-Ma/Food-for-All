from .functions import *

COOKIE_KEY = "apex"
COOKIE_EXPIRES = 7 * 24 * 60 * 60
COOKIE_PATH = "/"
COOKIE_SALT = "apex"

REGIS_CODE_EXPIRES = 30 * 60

REGION2RID, RID2REGION = create_region_list()
CURRENCY2CID, CID2CURRENCY = create_currency_list()
RID2CID = create_region_currency_list()
EXCHANGE_RATE = create_exchange_rate()
REGION2CURRENCY = dict([[RID2REGION[i], CID2CURRENCY[j]] for i,j in RID2CID.items()])

def region2rid(region):
    if region in REGION2RID:
        return REGION2RID[region]
    elif region in RID2REGION:
        return region
    else:
        return ""

def rid2region(rid):
    if rid2region in RID2REGION:
        return RID2REGION[rid2region]
    elif rid2region in REGION2RID:
        return rid2region
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