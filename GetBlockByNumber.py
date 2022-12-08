import json
import os
import threading
import time
from threading import Thread
from urllib.request import Request, urlopen
import OpenFile

latest_block_num = 16138610

# noinspection PyBroadException
def getMessageFromBlock(block_num):
    result = ""
    url = "https://api-cn.etherscan.com/api?module=proxy&action=eth_getBlockByNumber&tag="+ str(hex(block_num)) +"&boolean=true&apikey=NSDRFWGWMT6UUDEF44Y4HEF61QRU76WNGM"
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


def ScapyBlockData():
    last_block_num = readLastBlockNum()

    while True:
        last_block_num -= 1
        data = getMessageFromBlock(last_block_num)

        if 'status' in data :
            print("API Limit, retrying")
            time.sleep(1)
            last_block_num += 1
            continue

        print("downloading " + str(last_block_num) + " block data")
        OpenFile.writeFile("block_data/" + str(last_block_num) + ".json", json.dumps(data))


def main():

    thread_scapy_data = Thread(target=ScapyBlockData())
    thread_scapy_data.start()



if __name__ == "__main__":
    main()