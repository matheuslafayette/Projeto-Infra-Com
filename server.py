from rdt import *

users = {}
cont_bans = {}
users_ban = []

def main():
    server = Rdt('server', addrPort=13036)
    
    while True:
        
        print("The server is ready to receive!")
        server.reset_num_seq()
        
        msg, _ = server.rdt_rcv()
        msg = eval(msg.decode())
        addr = msg['addr']
        msg = msg['data']
        print(users)
        server.reset_num_seq()
        
        if msg.startswith('hi, meu nome eh '):
            newuser = msg.split('hi, meu nome eh ')[1]
            if newuser in users_ban:
                msg = "voce esta banido!"
                server.rdt_send(time_msg(msg), addr)
                continue
            for ad in users.keys():
                newmsg = newuser + ' entrou na sala!'
                server.rdt_send(time_msg(newmsg), ad)
                server.reset_num_seq()
            users[addr] = newuser
            cont_bans[newuser] = 0
        
        elif addr not in users.keys():
            msg = "voce ainda nao esta cadastrado!\n"
            server.rdt_send(msg, addr)
        
        elif msg == "bye":
            msg = "voce foi desconectado!\n"
            server.rdt_send(msg, addr)
            server.reset_num_seq()
            
            logoutuser = users[addr]
            logoutmsg = logoutuser + ' saiu da sala!'
            users.pop(addr)
            
            logoutmsg = time_msg(logoutmsg)
            
            for k in users.keys():               
                server.rdt_send(logoutmsg, k)
                server.reset_num_seq()
        
        elif msg == "list":
            listConnected = "\n"
            for user in users.values():
                listConnected += user + '\n'
            server.rdt_send(time_msg(listConnected), addr)
        
        elif msg.startswith("@"):
            msg = msg.removeprefix('@')
            userToSend, msg = msg.split(" ", 1)
            msg = time_msg(msg, users[addr])
            addrToSend, _ = find_by_value(userToSend)
            if addrToSend is not None:
                server.rdt_send(msg, addrToSend)
                    
        elif msg.startswith("ban"):
            ban_user = msg.split("@", 1)[1]
            try:
                cont_bans[ban_user] = cont_bans[ban_user] + 1
                if cont_bans[ban_user] >= len(users.values()) * 2 / 3:
                    ban_addr, _ = find_by_value(ban_user)
                    users.pop(ban_addr)
                    users_ban.append(ban_user)   
            except:
                continue                    
        
        else:
            msg = time_msg(msg, users[addr])
            for k in users.keys():
                if k != addr:
                    server.rdt_send(msg, k)
                    server.reset_num_seq()

def find_by_value(value):
    for k, v in users.items():
        if v == value:
            return (k, v)
    return None, None

def time_msg(msg, user = ""):
    ret = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + ":" + str(time.localtime().tm_sec) + " " + str(user) + ": " +str(msg) + '\n'
    return ret

if __name__ == "__main__":
    main()