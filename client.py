from rdt import *
import threading
import socket

host = socket.gethostbyname(socket.gethostname())
serverPort = 13024
clientPort = 5000
clientRcv = Rdt('client', addrPort=serverPort)

while True:
    try:
        serverRcv = Rdt('server', addrPort=clientPort)
        break
    except:
        clientPort += 1
        
addr = (host, clientPort)
        
lock = threading.Lock()

def rcv_data():
    while True:
        serverRcv.reset_num_seq()
        rcv_pkt, addr = serverRcv.rdt_rcv()
        msg = rcv_pkt.decode()
        print(msg)

def snd_data():
    while True:
        data = make_data(input('\n'))
        #print('\n')
        clientRcv.rdt_send(data, (host,serverPort))
        if data == "close":
            clientRcv.close()
            break
        clientRcv.reset_num_seq()

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