# -*- coding: utf-8 -*-
import requests
import json
import re
import time


LegendNumMin = 130

domain = 'shy.xzlol.cn'

GetAccountURL = f"https://{domain}/user/api/index/card"

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": f"https://{domain}/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
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
    "皮城警备": 68,
    "比尔吉沃特": 69,
    "德玛西亚": 70,
    "弗雷尔卓德": 71,
    "无畏先锋": 72,
    "扭曲丛林": 73,
    "巨龙之巢": 74,
    "恕瑞玛": 75,
    "男爵领域": 120
}

class Vniao:
    def __init__(self, server, page=None, cookies=None):
        self.page = 1
        if page is not None:
            self.page = page
        self.goodsid = server_dict.get(server)
        print(f"当前大区：{server}, 区号：{self.goodsid}\n")
        self.is_name_identify = False
        self.name_ind = 2
        self.legend_ind = 4
        self.cookies = cookies


    def GetAccounts(self):
        params = {
            "commodityId": self.goodsid,
            "page": self.page,
            "race": "",
        }

        for i in range(8):  # 循环去请求网站
            try:
                response = requests.get(GetAccountURL, headers=headers, params=params, timeout=(5, 7), cookies=self.cookies)
            except requests.RequestException as e:
                print(f"Vniao连接异常，尝试重新连接")
                time.sleep(5)
                continue
            if response.status_code == 200:
                break

        response_dict = json.loads(response.text)

        res = []
        heroNums = []
        card_ids = []

        if len(response_dict['data']['data']) == 0:
            return res, heroNums, card_ids, False
        # 格式为123456----影流----有情芍药含春泪丶#33586----等级:644----英雄:是167，请你改写上面的python代码|皮肤:270----单:白银Ⅲ胜点:59-最高段位:铂金|组:无-最高段位:白银----人脸:无----令牌:无----
        # for account in response_dict['data']['data']:
        #     tmp = account['draft'].split("----")
        #     name = tmp[2].split("#")[0]  # 提取名称，并去除#及其后面的内容
        #     if len(tmp[3].split(":")[-1]) == 0:
        #         continue
        #     LegendsNum = int((tmp[3].split("|")[0]).split(":")[-1])
        #     if LegendsNum < LegendNumMin:
        #         continue
        #     res.append(name)
        #     heroNums.append(LegendsNum)
        #     card_ids.append(account['id'])

        # 格式为影流----杀猪去00----等级:118----英雄:88|皮肤:12----单:无|组:无----人脸:无----令牌:无----
        for account in response_dict['data']['data']:
            tmp = account['draft'].split("----")
            if not self.is_name_identify:
                for index, item in enumerate(tmp):
                    if '英雄' in item:
                        self.legend_ind = index
                        self.name_ind = index - 2
                        self.is_name_identify = True
                        break

            name = tmp[self.name_ind].split("#")[0]
            if len(tmp[self.legend_ind].split(":")[-1]) == 0:
                continue
            LegendsNum = int((tmp[self.legend_ind].split("|")[0]).split(":")[-1])
            if LegendsNum < LegendNumMin:
                continue
            res.append(name)
            heroNums.append(LegendsNum)
            card_ids.append(f"-s {self.goodsid} -c {account['id']}")

        self.page += 1

        return res, heroNums, card_ids, True
