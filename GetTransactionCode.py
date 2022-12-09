import json
import os.path
import time
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
    # url = "https://api.etherscan.io/api?module=contract&action=getabi&address={}&apikey=YourApiKeyToken".format(address)
    url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey=NSDRFWGWMT6UUDEF44Y4HEF61QRU76WNGM".format(address=address)
    # headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    try:
        req = Request(url, headers=headers)
        response = urlopen(req,timeout=5).read()
        result = json.loads(response.decode())
    except Exception as exception:
        print(exception)
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
            # time.sleep(60)
            # continue
            break


def scapyTransactionCode():
    address_file_list = os.listdir("inputs")

    # for address_file in address_file_list:
    for i in range(0,len(address_file_list)):

        address_file = address_file_list[i]
        address = address_file[:-4]
        if os.path.exists("sol_code/" + address + ".json"):
            continue

        data = getTransactionCode(address)

        if data == "":
            i -= 1
            continue

        if 'status' in data:
            if data['status'] == "0":
                print("API Limit! Retrying")
                time.sleep(1)
                i -= 1
                continue
            else:
                if data['result'][0]['ABI'] == "Contract source code not verified" or data['result'][0]['SourceCode'] == "":
                    print("Contract source code not verified")
                    continue
        else:
            print("data does not have 'status'")
            continue

        print("downloading the contract :" + address)
        OpenFile.writeFile("sol_code/" + address + ".json",json.dumps(data))


if __name__ == "__main__":
    # parseTransactionAddressAndInput()
    scapyTransactionCode()