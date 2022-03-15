import csv
import os
from FoodForAll.settings import RESOURCE_PATH, BASE_DIR, STATIC_URL, IMG_PATH, DOC_PATH

region_list_file = os.path.join(RESOURCE_PATH, "region_list.csv")
currency_list_file = os.path.join(RESOURCE_PATH, "currency_list.csv")
region_currency_list_file = os.path.join(RESOURCE_PATH, "region_currency.csv")
exchange_rate_file = os.path.join(RESOURCE_PATH, "exchange_rate.csv")

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

def create_region_currency_list():
    with open(region_currency_list_file, "r", encoding="UTF-8") as f:
        region_currency_list = list(csv.reader(f))
    rid2cid = dict([i[:2] for i in region_currency_list])
    return rid2cid

def create_exchange_rate():
    with open(exchange_rate_file, "r", encoding="UTF-8") as f:
        exchange_rate_list = list(csv.reader(f))
        exchange_rate_list = [[i[0], float(i[1])] for i in exchange_rate_list]
    exchange_rate = dict([i[:2] for i in exchange_rate_list])
    return exchange_rate