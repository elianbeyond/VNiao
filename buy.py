# -*- coding: utf-8 -*-
import argparse

import requests
import json

parser = argparse.ArgumentParser(description='史迪仔买号')
parser.add_argument('-s', type=int, required=True, help='commodity_id')
parser.add_argument('-c', type=int, required=True, help='card_id')

args = parser.parse_args()


domain = f"gt.xzlol.cn"

TradeURL = f"https://{domain}/user/api/order/trade"
PayURL = f"https://{domain}"

headers = {
    # "authority": domain,
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "_aihecong_chat_channelIds=%5B%7B%22customerId%22%3A%2265c20798c505f02da2529374%22%2C%22channelId%22%3A%220IOt7b%22%7D%5D; __51vcke__KNgVAhHAvqA2au2f=7d2d1a6e-67b7-558f-a715-685b02532cad; __51vuft__KNgVAhHAvqA2au2f=1713276794198; guardok=u7F6HqSwTVKp9Ej8MzyrvsbPV64WcF7lpAj+cHYvWDHZgLh5f2N/Hk6UGJGJ4r9uUpYeregplcEtaSnqNgV/tA==; ACG-SHOP=gpud6lo7a52cicklc1tvu0ddht; _aihecong_chat_address=%7B%22city%22%3A%22%E8%A1%A1%E9%98%B3%22%2C%22region%22%3A%22%E6%B9%96%E5%8D%97%22%2C%22country%22%3A%22%E4%B8%AD%E5%9B%BD%22%7D; __vtins__KNgVAhHAvqA2au2f=%7B%22sid%22%3A%20%226b1be34b-0304-5859-9692-75ad815e1ff7%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201713787057052%2C%20%22ct%22%3A%201713785257052%7D; __51uvsct__KNgVAhHAvqA2au2f=5; _aihecong_chat_visibility=true",
    "origin": f"https://{domain}",
    "referer": f"https://{domain}/",
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}


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

response = requests.post(TradeURL, headers=headers, data=params, timeout=10)

response_dict = json.loads(response.content)

url = response_dict['data']['url']

print(PayURL + url)
