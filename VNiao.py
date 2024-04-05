import requests
import json
import re
import time


LegendNumMin = 130

Domain = "vn.vmp.cc"

GetAccountURL = f"https://16.xzlol.cn/user/api/index/card"

headers = {
    "authority": "https://16.xzlol.cn/",
    "method": "GET",
    "path": "/user/api/index/card?commodityId=50&page=2&race=",
    "scheme": "https",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": "_aihecong_chat_channelIds=%5B%7B%22customerId%22%3A%2265c1d0955924c703aa6cd75f%22%2C%22channelId%22%3A%220IOt7b%22%7D%5D; ACG-SHOP=h8aonhng1heeoeboto7mqegsn3; _aihecong_chat_visibility=true",
    "Referer": "https://16.xzlol.cn/",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "X-Requested-With": "XMLHttpRequest"
}


server_dict = {
    "艾欧尼亚": 50,
    "祖安": 51,
    "诺克萨斯": 52,
    "班德尔城": 53,
    "皮尔特沃夫": 54,
    "战争学院": 55,
    "巨神峰": 56,
    "雷瑟守备": 57,
    "裁决之地": 58,
    "黑色玫瑰": 59,
    "暗影岛": 60,
    "钢铁烈阳": 61,
    "水晶之痕": 62,
    "均衡教派": 63,
    "影流": 64,
    "守望之海": 65,
    "征服之海": 66,
    "卡拉曼达": 67,
    "皮城警备": 68
}



class Vniao:
    def __init__(self, server, page=None):
        self.page = 1
        if page is not None:
            self.page = page
        self.goodsid = server_dict.get(server)
        print(f"区号：{self.goodsid}\n")

    def GetAccounts(self):
        params = {
            "commodityId": self.goodsid,
            "page": self.page,
            "race": "",
        }

        for i in range(8):  # 循环去请求网站
            try:
                response = requests.post(GetAccountURL, headers=headers, params=params, timeout=(5, 7))
            except requests.RequestException as e:
                print(f"Vniao连接异常，尝试重新连接")
                time.sleep(5)
                continue
            if response.status_code == 200:
                break


        response_dict = json.loads(response.content)

        res = []
        heroNums = []
        card_ids = []

        if len(response_dict['data']['data']) == 0:
            return res, heroNums, card_ids, False

        for account in response_dict['data']['data']:
            tmp = account['draft'].split("----")
            name = tmp[1]
            if len(tmp[3].split(":")[-1]) == 0:
                continue
            LegendsNum = int(tmp[3].split(":")[-1])
            if LegendsNum < LegendNumMin:
                continue
            res.append(name)
            heroNums.append(LegendsNum)
            card_ids.append(account['id'])

        self.page += 1

        return res, heroNums, card_ids, True
