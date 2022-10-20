from rdt import *
import time

def main():
    
    client = Rdt('client')
    username = 'user'
    state = False
    
    while True:
                
        if not state:
            msg = input('mensagem: ')
            #client.rdt_send(msgsend)
            
            if msg == "bye":
                client.close()
                break
            
            state = ~state
        
        else:
            #receive from server
            True

if __name__ == "__main__":
    main()