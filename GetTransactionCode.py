import json
import OpenFile


def getTransactionAddressAndInput(block_num):
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
        if _input == "0x":
            continue
        # 以合约地址为名创建文件，其内存放输入信息
        OpenFile.appendFile("inputs/" + _address + ".txt", _input + "\n")

    OpenFile.writeFile("config/last_parse_block_num.txt", str(last_block_num - 1))
    return True



if __name__ == "__main__":
    last_block_num = int(OpenFile.openFileByString("config/last_parse_block_num.txt").strip())

    getTransactionAddressAndInput(last_block_num)