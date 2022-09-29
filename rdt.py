from socket import *
from common import *
class Rdt:
    
    def __init__(self, type : str, serverPort : int = 12000, serverName : str = 'localhost'):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.serverPort = serverPort
        self.serverName = serverName
        self.type = type
        self.num_seq_c = 0
        self.num_seq_s = 0
        
        if(type == 'server'):
            self.socket.bind(("", serverPort))
    
    def __del__(self):
        self.socket.close()
    
    def close(self):
        self.__del__()
    
    def send(self, data):
        
        if self.type == 'client':
            addr = (self.serverName, self.serverPort)
        else:
            addr = self.serverName

        if not isinstance(data, bytes):
            data = data.encode()
        
        print(data)
        
        self.socket.sendto(data, addr)
    
    def receive(self):
        if(self.type == 'client'):
            bytes_read = self.socket.recv(2048)
        else:
            bytes_read, self.serverName = self.socket.recvfrom(2048)
        return bytes_read
    
    def rdt_send(self, data):
        
        if not isinstance(data, bytes):
            data = data.encode()
        
        sum = checksum(data)
            
        sndpkt = make_pkt(data, sum, self.num_seq_c)
        sndpkt.encode()
        
        self.send(sndpkt)
        rcvpkt = self.rdt_rcv('wait_ack')
        
        while(not rcvpkt or corrupt(rcvpkt) or rcvpkt['num_seq'] != self.num_seq_c or not rcvpkt['is_ack']):
            self.send(sndpkt)
            rcvpkt = self.rdt_rcv('wait_ack')
        
        self.num_seq_c = 1 - self.num_seq_c
    
    def rdt_rcv(self, state : str = 'null'):
        
        if(state == 'wait_ack'):
            rcvpkt = eval(self.receive().decode())
            
            while(not rcvpkt or corrupt(rcvpkt) or rcvpkt['num_seq'] != self.num_seq_c):
                rcvpkt = eval(self.receive().decode())
            
            
        else:
            rcvpkt = eval(self.receive().decode())
            
            while(not rcvpkt or corrupt(rcvpkt) or rcvpkt['num_seq'] != self.num_seq_s):
                rcvpkt = eval(self.receive().decode())
                
            sndack = make_ack(self.num_seq_s)
            self.send(sndack)
            print('mandei ack')
            self.num_seq_s = 1 - self.num_seq_s
        
        return rcvpkt
        