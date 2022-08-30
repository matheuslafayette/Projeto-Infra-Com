from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print("The server is ready to receive")

while True:
    
    #recebe nome do arquivo
    filename, clientAddress = serverSocket.recvfrom(2048)
    filename = filename.decode()
    
    newFilename = "server-" + filename
    pathfile = "./" + newFilename

    #recebe arquivo do client
    with open(pathfile, "wb") as newFile:
        while True:
            bytes_read, clientAddress = serverSocket.recvfrom(2048)
            if not bytes_read:
                newFile.close()
                break
            newFile.write(bytes_read)


    #envia arquivo para o client
    with(open(pathfile, "rb")) as f:
        while True:
            bytes_read = f.read(2048)
            serverSocket.sendto(bytes_read, clientAddress)
            if not bytes_read:
                f.close()
                break