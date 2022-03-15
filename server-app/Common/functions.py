import csv
import os
from FoodForAll.settings import RESOURCE_DIR, BASE_DIR, STATIC_URL

region_list_file = os.path.join(RESOURCE_DIR, "region_list.csv")
currency_list_file = os.path.join(RESOURCE_DIR, "currency_list.csv")
exchange_rate_file = os.path.join(RESOURCE_DIR, "exchange_rate.csv")

def create_region_list():
    with open(region_list_file, "r", encoding="GBK") as f:
        region_list = list(csv.reader(f))
    region2rid = dict([i[:2][::-1] for i in region_list])
    rid2region = dict([i[:2] for i in region_list])
    return region2rid, rid2region

def create_currency_list():
    with open(currency_list_file, "r", encoding="GBK") as f:
        currency_list = list(csv.reader(f))
    currency2cid = dict([i[:2][::-1] for i in currency_list])
    cid2currency = dict([i[:2] for i in currency_list])
    return currency2cid, cid2currency

def create_exchange_rate():
    with open(exchange_rate_file, "r", encoding="UTF-8") as f:
        exchange_rate_list = list(csv.reader(f))
        exchange_rate_list = [[i[0], float(i[1])] for i in exchange_rate_list]
    exchange_rate = dict([i[:2] for i in exchange_rate_list])
    return exchange_rate
