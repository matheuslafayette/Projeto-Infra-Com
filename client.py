from socket import *
from rdt import *

def main():
    
    client = Rdt('client')
    
    filename = input("nome do arquivo: ")
    pathfile = "./arquivos-teste/" + filename
    
    client.rdt_send(filename)
    
    with(open(pathfile, "rb")) as file:
        while True:
            bytes_read = file.read(2048)
            client.rdt_send(bytes_read)
            if not bytes_read:
                file.close()
                break
    
    filename = "client-" + filename
    pathfile = "./client/" + filename
    
    with open(pathfile, "wb") as newFile:
        while True:
            bytes_read = client.rdt_rcv()['data']
            if not bytes_read:
                newFile.close()
                break   
            newFile.write(bytes_read)

if __name__ == "__main__":
    main()