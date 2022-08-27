from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print("The server is ready to receive")

received = serverSocket.recv(2048)
filename = received.decode()
filename = "./arquivos-teste/2-" + filename

with open(filename, "wb") as newFile:
    while True:
        bytes_read = serverSocket.recv(2048)
        if bytes_read:
            newFile.write(bytes_read)
        else:
            newFile.close()
            break
    
    # filesize = int(filesize)
    # modifiedFile = file.decode().upper()
    # serverSocket.sendto(modifiedFile.encode(), 
    #                     clientAddress)