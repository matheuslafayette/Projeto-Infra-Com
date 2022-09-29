from rdt import *

def main():
    server = Rdt('server')
    
    while True:
        
        print("The server is ready to receive")
        server.reset_num_seq()
        
        filename = server.rdt_rcv()['data'].decode()
        
        newFilename = "server-" + filename
        pathfile = "./server/" + newFilename
        
        with open(pathfile, "wb") as newFile:
            while True:
                bytes_read = server.rdt_rcv()['data']
                if not bytes_read:
                    newFile.close()
                    break
                newFile.write(bytes_read)
        
        print("arquivo recebido do client")
        
        with(open(pathfile, "rb")) as file:
            while True:
                bytes_read = file.read(1024)
                server.rdt_send(bytes_read)
                if not bytes_read:
                    file.close()
                    break
        
        print("arquivo enviado para o client")

if __name__ == "__main__":
    main()