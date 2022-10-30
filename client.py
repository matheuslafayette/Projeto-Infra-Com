from rdt import *
import threading
import socket
import time

host = socket.gethostbyname(socket.gethostname())
serverPort = 13024
clientPort = 5000
lastBan = None
secBan = 60
clientSnd = Rdt('client', addrPort=serverPort)

while True:
    try:
        clientRcv = Rdt('server', addrPort=clientPort)
        break
    except:
        clientPort += 1
        
addr = (host, clientPort)
        
lock = threading.Lock()

def rcv_data():
    while True:
        clientRcv.reset_num_seq()
        rcv_pkt, addr = clientRcv.rdt_rcv()
        msg = rcv_pkt.decode()
        print(msg)

def snd_data():
    while True:
        data = make_data(input('\n'))
        if lastBan != None and time.time() - lastBan < secBan:
            continue
        clientSnd.rdt_send(data, (host,serverPort))
        if data == "close":
            clientSnd.close()
            break
        clientSnd.reset_num_seq()

def make_data(msg):
    return str({
        'data': msg,
        'addr': addr
    })
    
def main():
    
    threading.Thread(target=snd_data).start()
    threading.Thread(target=rcv_data).start()
            
if __name__ == "__main__":
    main()