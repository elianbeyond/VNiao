# -*- coding: utf-8 -*-
import argparse

import requests
import json
from VNiao import domain, headers
from WeGame import cookie_str_to_dict

parser = argparse.ArgumentParser(description='史迪仔买号')
parser.add_argument('-s', type=int, required=True, help='commodity_id')
parser.add_argument('-c', type=int, required=True, help='card_id')

args = parser.parse_args()

TradeURL = f"https://{domain}/user/api/order/trade"
PayURL = f"https://{domain}"

cookie_str = "_aihecong_chat_channelIds=%5B%7B%22customerId%22%3A%2265c20798c505f02da2529374%22%2C%22channelId%22%3A%220IOt7b%22%7D%5D; __51vcke__KNgVAhHAvqA2au2f=7d2d1a6e-67b7-558f-a715-685b02532cad; __51vuft__KNgVAhHAvqA2au2f=1713276794198; ACG-SHOP=1h5lreu50t04f0imo9q8qe0vs2; guardok=6gjtK0zzt1u7wzUPxjBfSc5Ge7+jB0x863p2WpFJZOUmwcg9N4j5ep0YHYAAZgV6E04fwkxNUUaeJifdy3o3nA==; __51uvsct__KNgVAhHAvqA2au2f=13; _aihecong_chat_iframeopen=true; __vtins__KNgVAhHAvqA2au2f=%7B%22sid%22%3A%20%222cd1288b-99f5-54c0-a624-fa2ee2375aa9%22%2C%20%22vd%22%3A%202%2C%20%22stt%22%3A%208982%2C%20%22dr%22%3A%208982%2C%20%22expires%22%3A%201718116239012%2C%20%22ct%22%3A%201718114439012%7D; _aihecong_chat_visibility=true"

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
