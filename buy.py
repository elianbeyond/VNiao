# -*- coding: utf-8 -*-
import argparse

import requests
import json
from VNiao import domain, headers
from WeGame import cookie_str_to_dict
from get_cookie import get_vniao_cookie

parser = argparse.ArgumentParser(description='史迪仔买号')
parser.add_argument('-s', type=int, required=True, help='commodity_id')
parser.add_argument('-c', type=int, required=True, help='card_id')

args = parser.parse_args()

TradeURL = f"https://{domain}/user/api/order/trade"
PayURL = f"https://{domain}"

cookie_str = get_vniao_cookie()

commodity_id = args.s
card_id= args.c
params = {
    "contact": "88970615",
    "password": "88970615",
    "coupon": "",
    "num": "1",
    "captcha": "",
    "commodity_id": commodity_id,
    "card_id": card_id,
    "pay_id": "12",
    "device": "0",
    "from": "1596",
    "race": ""
    }

response = requests.post(TradeURL, headers=headers, data=params, cookies=cookie_str_to_dict(cookie_str), timeout=10)

response_dict = json.loads(response.content)

url = response_dict['data']['url']

print(PayURL + url)
