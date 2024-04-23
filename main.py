# -*- coding: utf-8 -*-
import time
import VNiao
import WeGame
import argparse
import concurrent.futures
import threading
from get_cookie import Driver


server_dict_inverse = {
    1: ["祖安", "皮尔特沃夫", "巨神峰", "男爵领域", "均衡教派", "影流", "守望之海"],
    2: ["卡拉曼达", "暗影岛", "征服之海", "诺克萨斯", "战争学院", "雷瑟守备"],
    3: ["班德尔城", "裁决之地", "水晶之痕", "钢铁烈阳", "皮城警备"],
    4: ["比尔吉沃特", "弗雷尔卓德", "扭曲丛林"],
    5: ["德玛西亚", "无畏先锋", "恕瑞玛", "巨龙之巢"],
    6: ["艾欧尼亚"],
    7: ["黑色玫瑰"],
}

# 创建一个事件对象，用于线程之间的通信
exit_event = threading.Event()


def get_results(server_name, page, output_file, driver):
    vniao = VNiao.Vniao(server_name, page)
    wegame = WeGame.Wegame(server_name, driver)

    output_file.write(f"大区：{server_name}\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        while not exit_event.is_set():
            if exit_event.is_set():
                break
            page_info = f"大海页数：{vniao.page - 1}到{vniao.page}"
            print(page_info)
            players, heroNums, card_ids, ok = vniao.GetAccounts()

            if not ok:
                break

            future = executor.submit(wegame.find_by_name_server_in_batch, players, heroNums, card_ids)
            futures.append(future)

            if len(futures) == 2:
                # Wait for the current batch of pages to finish before moving on
                concurrent.futures.wait(futures)
                for future in futures:
                    res = future.result()
                    output_file.write(page_info + "\n")
                    output_file.write("\n".join(res) + "\n")
                    output_file.flush()
                futures.clear()

    # Write the results of the remaining tasks to the file
    for future in futures:
        res = future.result()
        output_file.write(page_info + "\n")
        output_file.write("\n".join(res) + "\n")
        output_file.flush()

def main():
    print('''
    1: 联盟1区--祖安、皮尔特沃夫、巨神峰、男爵领域、均衡教派、影流、守望之海
    2: 联盟2区--卡拉曼达、暗影岛、征服之海、诺克萨斯、战争学院、雷瑟守备
    3: 联盟3区--班德尔城、裁决之地、水晶之痕、钢铁烈阳、皮城警备
    4: 联盟4区--比尔吉沃特、弗雷尔卓德、扭曲丛林
    5: 联盟5区--德玛西亚、无畏先锋、恕瑞玛、巨龙之巢
    6: 电1--艾欧尼亚
    7: 母1--黑色玫瑰
    ''')
    parser = argparse.ArgumentParser(description='大海助手')
    parser.add_argument('-s', type=int, required=True, help='服务器序号')
    parser.add_argument('-p', type=int, default=1, help='大海初始页数')
    # parser.add_argument('-c', type=str, required=True, help='cookies')

    args = parser.parse_args()

    server_names = server_dict_inverse.get(args.s)

    output_file = open(f"records/{time.strftime('%Y%m%d_%H%M%S', time.localtime())}_联盟{args.s}区.txt", "w")

    driver = Driver()
    driver.login()
    for server_name in server_names:
        get_results(server_name, args.p, output_file, driver)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("程序被强制中断，正在退出...")
        exit_event.set()
