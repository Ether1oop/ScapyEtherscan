import json
import os.path
from urllib.request import Request, urlopen
import OpenFile


latest_block_num = 16138610 # 2022.12.8


def getTransactionAddressAndInput(block_num):
    if not os.path.exists("block_data/" + str(block_num) + ".json"):
        return False

    block_str = OpenFile.openFileByString("block_data/" + str(block_num) + ".json")
    if block_str == "":
        print("Read File Error !")
        return False

    block_str = json.loads(block_str)
    if 'result' not in block_str:
        return False

    transaction_list = block_str['result']['transactions']
    for transaction in transaction_list:
        _address = transaction['to']
        _input = transaction['input']
        if _input == "0x" or _address is None:
            continue
        # 以合约地址为名创建文件，其内存放输入信息
        OpenFile.appendFile("inputs/" + _address + ".txt", _input + "\n")
    print("parsing block num :" + str(block_num))
    OpenFile.writeFile("config/last_parse_block_num.txt", str(block_num))
    return True


# noinspection PyBroadException
def getTransactionCode(address):
    result = ""
    url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey=NSDRFWGWMT6UUDEF44Y4HEF61QRU76WNGM".format(address=address)
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    try:
        req = Request(url, headers=headers)
        response = urlopen(req).read()
        result = json.loads(response.decode())
    except Exception:
        print(Exception)
    return result


def parseTransactionAddressAndInput():
    last_parse_block_num = OpenFile.openFileByString("config/last_parse_block_num.txt").strip()

    if last_parse_block_num == "":
        last_parse_block_num = latest_block_num + 1
    else:
        last_parse_block_num = int(last_parse_block_num)

    while True:
        flag = getTransactionAddressAndInput(last_parse_block_num - 1)
        last_parse_block_num -= 1
        if not flag:
            break


# def scapyTransactionCode():



if __name__ == "__main__":
    parseTransactionAddressAndInput()