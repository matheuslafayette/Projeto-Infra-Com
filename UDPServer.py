from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print("The server is ready to receive")

while True:
    
    received = serverSocket.recv(2048)
    filename = received.decode()
    filename = "2-" + filename
    pathfile = "./arquivos-teste/" + filename

    with open(pathfile, "wb") as newFile:
        while True:
            bytes_read = serverSocket.recv(2048)
            if not bytes_read:
                newFile.close()
                break
            newFile.write(bytes_read)