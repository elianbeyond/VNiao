import time

import requests
import json
import datetime
from tqdm import tqdm


# 净负场限制
NetLossMin = 10
#最近n小时限制
LastGameHours = 25


# 设置URL
SearchPlayerURL = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer"
GetBattleReportURL = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleReport"
GetPlayerRecentStat = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetPlayerRecentStat"
GetBattleListURL = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleList"
GetBattleDetailURL = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleDetail"

# 设置浏览器标头
headers = {
    "authority": "www.wegame.com.cn",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://www.wegame.com.cn",
    "referer": "https://www.wegame.com.cn/helper/lol/search/index.html?navid=61",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "trpc-caller": "wegame.pallas.web.LolBattle",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

server_dict = {
    "艾欧尼亚": 1,
    "比尔吉沃特": 2,
    "祖安": 3,
    "诺克萨斯": 4,
    "班德尔城": 5,
    "德玛西亚": 6,
    "皮尔特沃夫": 7,
    "战争学院": 8,
    "弗雷尔卓德": 9,
    "巨神峰": 10,
    "雷瑟守备": 11,
    "无畏先锋": 12,
    "裁决之地": 13,
    "黑色玫瑰": 14,
    "暗影岛": 15,
    "恕瑞玛": 16,
    "钢铁烈阳": 17,
    "水晶之痕": 18,
    "均衡教派": 19,
    "扭曲丛林": 20,
    "教育网专区": 21,
    "影流": 22,
    "守望之海": 23,
    "征服之海": 24,
    "卡拉曼达": 25,
    "巨龙之巢": 26,
    "皮城警备": 27,
    "男爵领域": 30,
    "峡谷之巅": 31
}


def cookie_str_to_dict(cookie_str) -> dict:
    cookie_dict = {}
    items = cookie_str.split(';')
    for item in items:
        key, value = item.split('=', 1)  # limit the split count to 1
        cookie_dict[key.strip()] = value.strip()  # remove leading/trailing spaces
    return cookie_dict


def postRetry(url, headers, cookies, data):
    response = []

    for i in range(4):  # 循环去请求网站
        try:
            response = requests.post(url, headers=headers, cookies=cookies, data=data, timeout=(5, 7))
        except requests.RequestException as e:
            print(f"连接异常，尝试重新连接")
            time.sleep(5)
            continue
        if response.status_code == 200:
            return response

    return response


class Wegame:

    def __init__(self, cookie_str, server_name):
        self.cookie = cookie_str_to_dict(cookie_str)
        self.server = server_dict.get(server_name)

    def get_battle_detail_by_game_id(self, id, game_id):
        data = {
            "account_type": 2,
            "id": id,
            "area": self.server,
            "game_id": game_id,
            "from_src": "lol_helper"
        }

        response = postRetry(GetBattleDetailURL, headers, self.cookie, json.dumps(data))

        response_dict = json.loads(response.content)
        if response_dict['battle_detail'] is None:
            return [], False
        battle_detail = response_dict['battle_detail']
        if battle_detail['player_details'] is None:
            return [], False
        player_details = battle_detail['player_details']
        if battle_detail['team_details'] is None:
            return [], False
        team_details = battle_detail['team_details']
        teams = {}
        for td in team_details:
            teams[td['teamId']] = []
        for pd in player_details:
            area_id = pd['translate_areaId']
            if len(area_id) == 0:
                area_id = self.server
            teams[pd['teamId']].append({'open_id':pd['openid'], 'area_id': area_id})

        # find the team containing the input id
        for v in teams.values():
            vv = []
            for x in v:
                vv.append(x['open_id'])
            if id not in vv:
                return v, True
        return [], False

    def get_recent_aram_battle_by_id(self, id):
        data = {
            "account_type": 2,
            "area": self.server,
            "from_src": "lol_helper",
            "filter": "aram",
            "id": id,
            "offset": 0
        }

        response = postRetry(GetBattleListURL, headers, self.cookie, json.dumps(data))
        response_dict = json.loads(response.content)
        if response_dict['battles'] is None:
            return "", False
        battles = response_dict['battles']
        if len(battles) == 0:
            return "", False
        battle = battles[0]
        if 'game_id' not in battle:
            return "", False
        game_id = battle['game_id']
        return game_id, True

    def _get_battle_report_by_id(self, id, name=None) -> (str, bool):
        data = {
            "account_type": 2,
            "area": self.server,
            "from_src": "lol_helper",
            "id": id,
            "sids": [255]
        }

        # 发送POST请求
        response = postRetry(GetBattleReportURL, headers, self.cookie, json.dumps(data))

        response_dict = json.loads(response.content)
        battle_count_dict = response_dict['battle_count']
        if battle_count_dict is None:
            return 1, 0, False
        arm_wins = battle_count_dict['total_arm_wins']
        arm_losts = battle_count_dict['total_arm_losts']
        return arm_wins, arm_losts, True

    def _get_battle_report_by_dict(self, d, name=None) -> (str, bool):
        data = {
            "account_type": 2,
            "area": d['area_id'],
            "from_src": "lol_helper",
            "id": d['open_id'],
            "sids": [255]
        }

        # 发送POST请求
        response = postRetry(GetBattleReportURL, headers, self.cookie, json.dumps(data))

        response_dict = json.loads(response.content)
        battle_count_dict = response_dict['battle_count']
        if battle_count_dict is None:
            return 1, 0, False
        arm_wins = battle_count_dict['total_arm_wins']
        arm_losts = battle_count_dict['total_arm_losts']
        return arm_wins, arm_losts, True

    def _get_recent_game_time(self, id) -> str:
        data = {
            "account_type": 2,
            "area": self.server,
            "from_src": "lol_helper",
            "id": id,
        }
        # 发送POST请求
        response = postRetry(GetPlayerRecentStat, headers, self.cookie, json.dumps(data))
        response_dict = json.loads(response.content)

        recent_state = response_dict['recent_state']
        last_game_time = int(recent_state['last_game_time'])
        timestamp = last_game_time / 1000  # 转换为秒
        date = datetime.datetime.fromtimestamp(timestamp)
        # 如果最近一场游戏是在4小时内，则不发送消息
        total_hours = (datetime.datetime.now() - date).total_seconds() / 3600
        if total_hours < LastGameHours:
            # 如果最近一场游戏是在 LastGameHours 小时内，则不发送消息
            return ""

        formatted_date = date.strftime("%Y年%m月%d日%p%I点%M分")
        # 将 AM/PM 转换为 "上午" 或 "下午"
        formatted_date = formatted_date.replace('AM', '上午').replace('PM', '下午')
        return formatted_date

    def _get_info_by_name(self, name) -> list:
        data = {
            "nickname": name,
            "from_src": "lol_helper"
        }
        while True:
            # 发送POST请求
            response = postRetry(SearchPlayerURL, headers, self.cookie, json.dumps(data))
            response_dict = json.loads(response.content)
            if response_dict['result']['error_code'] == 8000022:
                if input(
                        f"机器验证，扣1重试，其他跳过，重试链接：https://www.wegame.com.cn/helper/lol/frame.html?navid=27 ") == '1':
                    continue
            if response_dict['players'] is None:
                print(response.content)
                return []
            else:
                return response_dict['players']
        return []

    def find_by_name_server(self, name, heroNum, card_id) -> (str, bool):
        players = self._get_info_by_name(name)
        if len(players) == 0:
            print(f"未找到该ID:{name}")
            return "", False

        for player in players:
            if player['area'] == self.server:
                aram_wins, aram_losts, isSuccess = self._get_battle_report_by_id(player['openid'], name)
                if not isSuccess:
                    return "", False
                net_loss = aram_losts - aram_wins
                if net_loss >= NetLossMin:
                    last_game_time = self._get_recent_game_time(player['openid'])
                    if last_game_time == "":
                        return "", False

                    res = f"Name: {name}, HeroNum: {heroNum}, Rate: {aram_wins / (aram_wins + aram_losts):.2%},Win: {aram_wins}, Loss: {aram_losts}, Net Loss: {net_loss}," \
                          f" Last Game Time: {last_game_time}, Card id: {card_id}\n"
                    game_id, isSuccess = self.get_recent_aram_battle_by_id(player['openid'])
                    if not isSuccess:
                        return "", False
                    enemies, isSuccess = self.get_battle_detail_by_game_id(player['openid'], game_id)
                    if not isSuccess:
                        return "", False
                    win_rate = []
                    for enemy in enemies:
                        win, lose, isSuccess = self. _get_battle_report_by_dict(enemy)
                        if not isSuccess:
                            win_rate.append("隐藏狗")
                        else:
                            if win + lose == 0:
                                win_rate.append("没有记录")
                            else:
                                win_rate.append(f"{win / (win + lose) * 100:.1f}%")
                    res += " ".join(win_rate)
                    res += '\n'
                    print(res)
                    return res, True
                else:
                    return "", False
        print(f"未找到该ID:{name}")
        return "", False

    def find_by_name_server_in_batch(self, names, heroNums, card_ids) -> list:
        res = []
        index = 0
        for name in tqdm(names):
            heroNum = heroNums[index]
            card_id = card_ids[index]
            index = index + 1
            battle_report, found = self.find_by_name_server(name, heroNum, card_id)
            if found:
                res.append(battle_report)
            # 防止API被封
            # time.sleep(1)

        return res
