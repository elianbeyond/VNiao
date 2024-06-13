import requests
import json
import re
import time


LegendNumMin = 130

domain = "vn.vmp.cc"
GetAccountURL = f"https://wn.vmp.cc/shop/shop/getAccount"

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
    "艾欧尼亚": 51981,  # 从班德尔城的下一个值开始
    "祖安": 51977,
    "诺克萨斯": 51983,
    "班德尔城": 51979,  # 保持不变
    "皮尔特沃夫": 51980,  # 保持不变
    "战争学院": 51984,
    "巨神峰": 51981,
    "雷瑟守备": 51986,
    "裁决之地": 51987,
    "黑色玫瑰": 51988,
    "暗影岛": 51989,
    "钢铁烈阳": 51990,
    "水晶之痕": 51991,
    "均衡教派": 51992,
    "影流": 51989,
    "守望之海": 51990,
    "征服之海": 51995,
    "卡拉曼达": 51996,
    "皮城警备": 51997  # 假设这是最后一个服务器，值继续递增
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
            "userid": "50",
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
            name = tmp['3'].split("#")[0]
            LegendsNum = int(tmp['4'].split("英雄:")[-1].split('----')[0])
            if LegendsNum < LegendNumMin:
                continue
            res.append(name)
            heroNums.append(LegendsNum)

        self.page += 1

        return res, heroNums, True
