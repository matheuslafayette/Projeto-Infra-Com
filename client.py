from rdt import *
import threading
import socket

host = socket.gethostbyname(socket.gethostname())
serverPort = 13009
clientPort = 5000

while True:
    try:
        clientRcv = Rdt('server', addrPort=clientPort)
        break
    except:
        clientPort += 1
        
lock = threading.Lock()

def rcv_data():
    while True:
        clientRcv.reset_num_seq()
        rcv_pkt, addr = clientRcv.udt_rcv()
        msg = rcv_pkt.decode()
        print(msg)

def snd_data():
    while True:
        data = input()
        clientRcv.udt_send(data, (host, serverPort))
        if data == "close":
            clientRcv.close()
            break
        clientRcv.reset_num_seq()
    
def main():
    
    username = 'user'
    threading.Thread(target=snd_data).start()
    threading.Thread(target=rcv_data).start()
            
if __name__ == "__main__":
    main()