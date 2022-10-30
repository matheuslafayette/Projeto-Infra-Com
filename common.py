from socket import *
import time

def checksum(data):
    
        addr = 0 
        sum = 0

        count = len(data)
        while (count > 1):
            sum += data[addr] << 8 + data[addr+1]
            addr += 2
            count -= 2
            
        if (count > 0):
            sum += data[addr]

        while (sum>>16):
            sum = (sum & 0xffff) + (sum >> 16)

        checksum = ~sum
        return checksum

def make_pkt(data, checksum, num_seq):
    return str({
        'data': data,
        'checksum': checksum,
        'num_seq': num_seq,
        'is_ack': False
    })

def make_ack(num_seq):
    return str({
        'data': "ACK",
        'num_seq': num_seq,
        'checksum': checksum("ACK".encode()),
        'is_ack': True
    })

def corrupt(pkt):
    try:
        return pkt['checksum'] != checksum(pkt['data'])
    except:
        return pkt['checksum'] != checksum(pkt['data'].encode())

