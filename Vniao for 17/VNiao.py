import requests
import json
import re
import time
from datetime import datetime, timedelta

LegendNumMin = 80

Domain = "vn.vmp.cc"

GetAccountURL = f"https://luck.edri.cc/shop/shop/getAccount"


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Length": "58",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_aihecong_chat_address=%7B%22city%22%3A%22%E7%9B%8A%E9%98%B3%22%2C%22region%22%3A%22%E6%B9%96%E5%8D%97%22%2C%22country%22%3A%22%E4%B8%AD%E5%9B%BD%22%7D; _aihecong_chat_channelIds=%5B%7B%22customerId%22%3A%2265a0e326233ea92c4b670354%22%2C%22channelId%22%3A%22u01BvN%22%7D%5D; s80bd7f1b=ma1sbq0f3qeq590k04mmo6glbr; Hm_lvt_6042ca82bb3b80dda6c78e835e7b26cc=1705042723,1705063591,1705119347; _aihecong_chat_iframeopen=true; _aihecong_chat_conversation=true; Hm_lpvt_6042ca82bb3b80dda6c78e835e7b26cc=1705119698; _aihecong_chat_visibility=true",
    "Host": "luck.edri.cc",
    "Origin": "https://luck.edri.cc",
    "Referer": "https://luck.edri.cc/links/3612B1EC",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows"
}

server_dict = {
    "艾欧尼亚": 43710,
    "祖安": 43711,
    "诺克萨斯": 43712,
    "班德尔城": 43713,
    "皮尔特沃夫": 43714,
    "战争学院": 43715,
    "巨神峰": 43716,
    "雷瑟守备": 43717,
    "裁决之地": 43718,
    "黑色玫瑰": 43719,
    "暗影岛": 43720,
    "钢铁烈阳": 43721,
    "水晶之痕": 43722,
    "均衡教派": 43723,
    "影流": 43724,
    "守望之海": 43725,
    "征服之海": 43726,
    "卡拉曼达": 43727,
    "皮城警备": 43728
}


class Vniao:
    def __init__(self, server, page=None):
        self.page = 1
        if page is not None:
            self.page = page
        self.goodsid = server_dict.get(server)

    def GetAccounts(self):
        data = {
            "agent_goodsid": self.goodsid,
            "goodsid": self.goodsid - 42096,
            "page": self.page,
            "userid": "1120",
            "type": "new"
        }

        # 发送POST请求

        try:
            response = requests.post(GetAccountURL, headers=headers, data=data, timeout=(10, 15))
        except:
            for i in range(4):  # 循环去请求网站
                print(f"连接异常，尝试重新连接")
                time.sleep(5)
                response = requests.post(GetAccountURL, headers=headers, data=data, timeout=(10, 15))
                if response.status_code == 200:
                    break

        response_dict = json.loads(response.content)

        res = []
        heroNums = []

        if len(response_dict['data']) == 0:
            return res, heroNums, False

        for account in response_dict['data']:
            tmp = account['number']
            name = tmp['3']

            hero_info = tmp["4"]
            hero_details = hero_info.split("----")  # 使用字符串分割操作符"----"分割英雄信息字符串
            # 提取等级、英雄和皮肤信息
            for detail in hero_details:
                if "等级:" in detail:
                    level = re.search(r'等级:(\d+)', detail).group(1)
                elif "英雄:" in detail:
                    hero = re.search(r'英雄:(\d+)', detail).group(1)
                    if int(hero) > LegendNumMin:
                        res.append(name)
                        heroNums.append(hero)
                        continue



        self.page += 1

        return res, heroNums, True


