def checksum(data):
    
        #RFC 1071
        addr = 0 
        Sum = 0

        count = len(data)
        while (count > 1):
            Sum += data[addr] << 8 + data[addr+1]
            addr += 2
            count -= 2
            
        if (count > 0):
            Sum += data[addr]

        while (Sum>>16):
            Sum = (Sum & 0xffff) + (Sum >> 16)

        checksum = ~Sum
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

