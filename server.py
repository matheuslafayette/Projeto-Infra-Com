from socket import *
from rdt import *

def main():
    server = Rdt('server')
    
    while True:
        print("server ready")
        filename = server.rdt_rcv()['data'].decode()
        print(filename)
        
        newFilename = "server-" + filename
        pathfile = "./server/" + newFilename
        
        with open(pathfile, "wb") as newFile:
            while True:
                bytes_read = server.rdt_rcv()['data']
                if not bytes_read:
                    newFile.close()
                    break
                newFile.write(bytes_read)
        
        with(open(pathfile, "rb")) as file:
            while True:
                bytes_read = file.read(2048)
                server.rdt_send(bytes_read)
                if not bytes_read:
                    file.close()
                    break

if __name__ == "__main__":
    main()