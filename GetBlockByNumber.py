import json
import os
import time
from urllib.request import Request, urlopen
import OpenFile

latest_block_num = 16138610 # 2022.12.8

# noinspection PyBroadException
def getMessageFromBlock(block_num):
    result = ""
    url = "https://api-cn.etherscan.com/api?module=proxy&action=eth_getBlockByNumber&tag={}&boolean=true&apikey=NSDRFWGWMT6UUDEF44Y4HEF61QRU76WNGM".format(str(hex(block_num)))
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    try:
        req = Request(url, headers=headers)
        response = urlopen(req).read()
        result = json.loads(response.decode())
    except Exception:
        print(Exception)
    return result


def readLastBlockNum():
    block_list = os.listdir("block_data")

    if len(block_list) == 0:
        # 表示要从最新区块号开始爬取
        last_block_num = latest_block_num + 1 # 后面会从last_block_num - 1开始爬取
    else:
        # 否则从编号最小的块继续爬取
        block_list.sort(key=lambda x: x[:-5])
        last_block_num = int(block_list[0][:-5])

    return last_block_num


def _readLastBlockNum():
    last_block_num = OpenFile.openFileByString("config/last_scapy_block_num.txt").strip()
    if last_block_num == "":
        return latest_block_num + 1
    else:
        return int(last_block_num)


def ScapyBlockData():
    last_block_num = _readLastBlockNum()

    while True:
        last_block_num -= 1
        data = getMessageFromBlock(last_block_num)

        if 'status' in data : # 此处可优化
            print("API Limit, retrying")
            time.sleep(1)
            last_block_num += 1
            continue

        print("downloading " + str(last_block_num) + " block data")
        OpenFile.writeFile("block_data/" + str(last_block_num) + ".json", json.dumps(data))
        OpenFile.writeFile("config/last_scapy_block_num.txt", str(last_block_num))


