from threading import Thread
import GetBlockByNumber

def main():

    thread_scapy_data = Thread(target=GetBlockByNumber.ScapyBlockData())
    thread_scapy_data.start()



if __name__ == "__main__":
    main()