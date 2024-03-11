import time
import VNiao
import WeGame
import argparse
import concurrent.futures
import threading

server_dict_inverse = {
    1: "艾欧尼亚",
    2: "祖安",
    3: "诺克萨斯",
    4: "班德尔城",
    5: "皮尔特沃夫",
    6: "战争学院",
    7: "巨神峰",
    8: "雷瑟守备",
    9: "裁决之地",
    10: "黑色玫瑰",
    11: "暗影岛",
    12: "钢铁烈阳",
    13: "水晶之痕",
    14: "均衡教派",
    15: "影流",
    16: "守望之海",
    17: "征服之海",
    18: "卡拉曼达",
    19: "皮城警备"
}

# 创建一个事件对象，用于线程之间的通信
exit_event = threading.Event()

def get_results(server_no, page, cookie_str):
    server_name = server_dict_inverse.get(server_no)
    vniao = VNiao.Vniao(server_name, page)
    wegame = WeGame.Wegame(cookie_str, server_name)

    output_file = open(f"records/{time.strftime('%Y%m%d_%H%M%S', time.localtime())}_{server_name}.txt", "w")

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            while not exit_event.is_set():
                if exit_event.is_set():
                    break
                page_info = f"大海页数：{vniao.page-1}到{vniao.page}"
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
                    futures.clear()

        # Write the results of the remaining tasks to the file
        for future in futures:
            res = future.result()
            output_file.write(page_info + "\n")
            output_file.write("\n".join(res) + "\n")

    except KeyboardInterrupt:
        print("程序被强制中断，正在关闭文件...")
        output_file.close()
        print("文件已关闭,记录已保存。")
        return

    output_file.close()

def main():
    print('''
    1: "艾欧尼亚",2: "祖安",3: "诺克萨斯",4: "班德尔城",
    5: "皮尔特沃夫",6: "战争学院",7: "巨神峰",8: "雷瑟守备",
    9: "裁决之地",10: "黑色玫瑰",11: "暗影岛",12: "钢铁烈阳",
    13: "水晶之痕",14: "均衡教派",15: "影流",16: "守望之海",
    17: "征服之海",18: "卡拉曼达",19: "皮城警备"
    ''')
    parser = argparse.ArgumentParser(description='大海助手')
    parser.add_argument('-s', type=int, required=True, help='服务器序号')
    parser.add_argument('-p', type=int, default=1, help='大海初始页数')
    parser.add_argument('-c', type=str, required=True, help='cookies')

    args = parser.parse_args()

    get_results(args.s, args.p, args.c)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("程序被强制中断，正在退出...")
        exit_event.set()
