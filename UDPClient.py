from socket import *
import os

serverName = '10.0.0.112'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

filename = "TestePDF.pdf"
pathfile = "./arquivos-teste/" + filename

file = open(pathfile)

clientSocket.sendto(f"{filename}".encode(), (serverName, serverPort))

with(open(pathfile, "rb")) as f:
    while True:
        bytes_read = f.read(2048)
        if bytes_read:
            clientSocket.sendto(bytes_read, (serverName, serverPort))
        else:
            f.close()
            break
        

clientSocket.close()