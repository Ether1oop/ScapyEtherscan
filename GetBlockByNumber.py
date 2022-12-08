import os
import time
from urllib.request import Request, urlopen
import OpenFile

# http://api-cn.etherscan.com/api?module=proxy&action=eth_getBlockByNumber&tag="+ str(hex(latest_blocknum - i)) +"&boolean=true&apikey=YourApiKeyToken
latest_block_num = 16138610

# noinspection PyBroadException
def getMessageFromBlock(block_num):
    result = ""
    url = "https://api-cn.etherscan.com/api?module=proxy&action=eth_getBlockByNumber&tag="+ str(hex(block_num)) +"&boolean=true&apikey=YourApiKeyToken"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
    try:
        req = Request(url, headers=headers)
        response = urlopen(req).read()
        # result = json.loads(response.decode())
        result = response.decode()
    except Exception:
        print("API Limit, retrying \n")
        time.sleep(1)
    print("downloading " + str(block_num) + " block data")
    return result


def readLastBlockNum():
    block_list = os.listdir("block_data")

    if len(block_list) == 0:
        # 表示要从最新区块号开始爬取
        last_block_num = latest_block_num + 1 # 后面会从last_block_num - 1开始爬取
    else:
        block_list.sort(key=lambda x: x[:-5])
        last_block_num = int(block_list[0][:-5])

    return last_block_num

def main():
    last_block_num = readLastBlockNum()
    while True:
        last_block_num -= 1
        data = getMessageFromBlock(last_block_num)
        OpenFile.writeFile("block_data/" + str(last_block_num) + ".json", data)


if __name__ == "__main__":
    main()