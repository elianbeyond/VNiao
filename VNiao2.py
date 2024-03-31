import requests
import json
import re
import time


LegendNumMin = 130

Domain = "vn.vmp.cc"

GetAccountURL = f"https://mx.youyoupay.com/getKaAccount"

headers = {
##    "authority": Domain,
##    "accept": "*/*",
##    "accept-language": "zh-CN,zh;q=0.9",
##    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
##    "origin": f"https://{Domain}",
##    "referer": f"https://{Domain}//vniao/C034711D",
##    "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
##    "sec-ch-ua-mobile": "?0",
##    "sec-ch-ua-platform": '"macOS"',
##    "sec-fetch-dest": "empty",
##    "sec-fetch-mode": "cors",
##    "sec-fetch-site": "same-origin",
##    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
##    "x-requested-with": "XMLHttpRequest"
}

server_dict = {
    "艾欧尼亚": 1545,
    "祖安": 1546,
    "诺克萨斯": 1547,
    "班德尔城": 1548,
    "皮尔特沃夫": 1551,
    "战争学院": 1550,
    "巨神峰": 1549,
    "雷瑟守备": 1552,
    "裁决之地": 1553,
    "黑色玫瑰": 1554,
    "暗影岛": 1555,
    "钢铁烈阳": 1556,
    "水晶之痕": 1557,
    "均衡教派": 1558,
    "影流": 1559,
    "守望之海": 1560,
    "征服之海": 1561,
    "卡拉曼达": 1562,
    "皮城警备": 1576
}


class Vniao:
    def __init__(self, server, page=None):
        self.page = 1
        if page is not None:
            self.page = page
        self.goodsid = server_dict.get(server)

    def GetAccounts(self):
        data = {
            "goodsid": self.goodsid,
            "page": self.page,
            "userid": "xUg49hDmDb7esMzNDeZ5Yg==",
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
            return res, heroNums ,False

        for account in response_dict['data']:
            tmp = account['number']
            name = tmp['3']
            LegendsNum = int(tmp['5'].split("英雄:")[-1].split('|')[0])
            if LegendsNum < LegendNumMin:
                continue
            res.append(name)
            heroNums.append(LegendsNum)

        self.page += 1

        return res, heroNums, True
