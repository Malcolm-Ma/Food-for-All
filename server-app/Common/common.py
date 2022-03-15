from .functions import *

DEFAULT_AVATAR = os.path.join(STATIC_URL, "default.jpg")

COOKIE_EXPIRES = 7 * 24 * 60 * 60
COOKIE_PATH = "/"
COOKIE_SALT = "apex"

REGIS_CODE_EXPIRES = 30 * 60

REGION2RID, RID2REGION = create_region_list()
CURRENCY2CID, CID2CURRENCY = create_currency_list()
EXCHANGE_RATE = create_exchange_rate()