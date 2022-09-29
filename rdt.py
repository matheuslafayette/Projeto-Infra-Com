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
    
    def reset_num_seq(self):
        self.num_seq_c = 0
        self.num_seq_s = 0
    
    def close(self):
        self.__del__()
    
    def udt_send(self, data):
        
        if self.type == 'client':
            addr = (self.serverName, self.serverPort)
        else:
            addr = self.serverName

        if not isinstance(data, bytes):
            data = data.encode()
        
        #print(data)
        
        self.socket.sendto(data, addr)
    
    def udt_rcv(self):
        if(self.type == 'client'):
            bytes_read = self.socket.recv(4096)
        else:
            bytes_read, self.serverName = self.socket.recvfrom(4096)
        return bytes_read
    
    def rdt_send(self, data):
        
        if not isinstance(data, bytes):
            data = data.encode()
        
        sum = checksum(data)
        sndpkt = make_pkt(data, sum, self.num_seq_c)
        sndpkt.encode()

        rcvpkt = None
        while(not rcvpkt or corrupt(rcvpkt) or rcvpkt['num_seq'] != self.num_seq_c or not rcvpkt['is_ack']):
            self.socket.settimeout(1)
            self.udt_send(sndpkt)
            try:
                rcvpkt = self.rdt_rcv('wait_ack')
            except socket.timeout:
                continue
            else:
                self.socket.settimeout(None)
                break
        
        self.num_seq_c = 1 - self.num_seq_c
    
    def rdt_rcv(self, state : str = 'null'):
        
        if(state == 'wait_ack'):
            rcvpkt = None
            while(not rcvpkt or corrupt(rcvpkt) or rcvpkt['num_seq'] != self.num_seq_c):
                rcvpkt = eval(self.udt_rcv().decode())
            
        else:
            rcvpkt = None
            while(not rcvpkt or corrupt(rcvpkt) or rcvpkt['num_seq'] != self.num_seq_s):
                rcvpkt = eval(self.udt_rcv().decode())
                
            sndack = make_ack(self.num_seq_s)
            self.udt_send(sndack)
            #print('send ack')
            self.num_seq_s = 1 - self.num_seq_s
        
        return rcvpkt
        