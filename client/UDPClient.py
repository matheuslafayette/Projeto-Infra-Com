from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

filename = input("nome do arquivo: ")
pathfile = "./../arquivos-teste/" + filename

#envia nome do arquivo
clientSocket.sendto(f"{filename}".encode(), (serverName, serverPort))

#envia arquivo para o servidor
with(open(pathfile, "rb")) as f:
    while True:
        bytes_read = f.read(2048)
        clientSocket.sendto(bytes_read, (serverName, serverPort))
        if not bytes_read:
            f.close()
            break

filename = "client-" + filename
pathfile = "./" + filename

#recebe o arquivo do servidor
with open(pathfile, "wb") as newFile:
    while True:
        bytes_read = clientSocket.recv(2048) #bytes_read = serverSocket.recv(2048)
        if not bytes_read:
            newFile.close()
            break
        newFile.write(bytes_read)

clientSocket.close()