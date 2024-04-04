# -*- coding: utf-8 -*-
import argparse

import requests
import json
import re
import time
import zlib
from urllib.parse import urlencode

TradeURL = f"https://16.xzlol.cn/user/api/order/trade"
PayURL = f"https://16.xzlol.cn"

headers = {
    "authority": "16.xzlol.cn",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "_aihecong_chat_channelIds=%5B%7B%22customerId%22%3A%2265e854d4cd3bde47891d0e5d%22%2C%22channelId%22%3A%220IOt7b%22%7D%5D; ACG-SHOP=ra91bpd983fke9dj2isgjiqhen; _aihecong_chat_address=%7B%22city%22%3A%22%E5%B9%BF%E5%B7%9E%22%2C%22region%22%3A%22%E5%B9%BF%E4%B8%9C%22%2C%22country%22%3A%22%E4%B8%AD%E5%9B%BD%22%7D; _aihecong_chat_visibility=true",
    "origin": "https://16.xzlol.cn",
    "referer": "https://16.xzlol.cn/",
    "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}


parser = argparse.ArgumentParser(description='史迪仔买号')
parser.add_argument('-s', type=int, required=True, help='commodity_id')
parser.add_argument('-c', type=int, required=True, help='card_id')

args = parser.parse_args()

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
    "from": "1220",
    "race": ""
    }

response = requests.post(TradeURL, headers=headers, data=params, timeout=(5, 7))

response_dict = json.loads(response.content)

url = response_dict['data']['url']

print(PayURL + url)