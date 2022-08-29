from socket import *

serverName = '10.0.0.112'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

filename = "TesteTXT.txt"
pathfile = "./arquivos-teste/" + filename

clientSocket.sendto(f"{filename}".encode(), (serverName, serverPort))

with(open(pathfile, "rb")) as f:
    while True:
        bytes_read = f.read(2048)
        clientSocket.sendto(bytes_read, (serverName, serverPort))
        if not bytes_read:
            f.close()
            break

clientSocket.close()