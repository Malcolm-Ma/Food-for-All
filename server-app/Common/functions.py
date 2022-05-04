import csv
import os
from FoodForAll.settings import RESOURCE_DIR, BASE_DIR, STATIC_URL, IMG_DIR, DOC_DIR, STATUS_CODE, VERIFY_CODE_EXPIRES, VERIFY_CODE_KEY_REGIS, VERIFY_CODE_KEY_RESET_PASSWORD, MAX_FAILED_LOGIN_ATTEMPTS_KEY, LOGIN_FORBIDDEN_KEY, MAX_FAILED_LOGIN_ATTEMPTS_ALLOWED, MAX_FAILED_LOGIN_INTERVAL_ALLOWED
import time
from hashlib import md5
import sys
from functools import wraps
import random
import re
import base64 as b64
import json
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.core.cache import caches
import string
from Mail.models import Mail
import requests

region_list_file = os.path.join(RESOURCE_DIR, "region_list.csv")
currency_list_file = os.path.join(RESOURCE_DIR, "currency_list.csv")
region_currency_list_file = os.path.join(RESOURCE_DIR, "region_currency.csv")
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