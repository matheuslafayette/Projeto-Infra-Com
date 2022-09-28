from socket import *
from common import *

class Rdt:
    
    def __init__(self, type : str, serverPort : int = 12000, serverName : str = 'localhost'):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.serverPort = serverPort
        self.serverName = serverName
        self.type = type
        self.num_seq = 0
        
        if(type == 'server'):
            self.socket.bind(("", serverPort))
    
    def __del__(self):
        self.socket.close()
    
    def send(self, data):
        
        if self.type == 'client':
            addr = (self.serverName, self.serverPort)
        else:
            addr = self.serverName

        if not isinstance(data, bytes):
            data = data.encode()
        
        print(data)
        print(type(data))
        self.socket.sendto(data, addr)
        print("foixd")
    
    def receive(self):
        bytes_read, self.serverName = self.socket.recvfrom(2048)
        return bytes_read
    
    def rdt_send(self, data):
        
        if isinstance(data, bytes):
            data = data.decode()
        
        data = data.encode()
        
        sum = checksum(data)
            
        sndpkt = make_pkt(data, sum, self.num_seq)
        sndpkt.encode()
        
        rcvpkt = None
        
        while(not rcvpkt or corrupt(rcvpkt) or rcvpkt['num_seq'] != self.num_seq or not rcvpkt['is_ack']):
            self.send(sndpkt)
            rcvpkt = self.rdt_rcv()
        
        self.num_seq = 1 - self.num_seq
    
    def rdt_rcv(self):
        
        rcvpkt = eval(self.receive().decode())
        
        while(not rcvpkt or corrupt(rcvpkt) or rcvpkt['num_seq'] != self.num_seq):
            rcvpkt = eval(self.receive().decode())
        
        if(self.type == 'server'):
            sndack = make_ack(self.num_seq)
            self.send(sndack)
            print('mandei ack')
        
        return rcvpkt
        