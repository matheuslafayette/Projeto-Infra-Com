from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print("The server is ready to receive")

#Recebe do client
while True:
    
    received, clientAddress = serverSocket.recvfrom(2048)
    filename = received.decode()
    newFilename = "2-" + filename
    pathfile = "./arquivos-teste/" + newFilename

    with open(pathfile, "wb") as newFile:
        while True:
            bytes_read = serverSocket.recv(2048)
            if not bytes_read:
                newFile.close()
                break
            newFile.write(bytes_read)

    
    #Envia de volta ao cliente
    with(open(pathfile, "rb")) as f:
        while True:
            bytes_read = f.read(2048)
            serverSocket.sendto(bytes_read, clientAddress)
            if not bytes_read:
                f.close()
                break