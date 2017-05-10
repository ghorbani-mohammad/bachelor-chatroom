from socket import *
serverPort=12001
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
while 1:
    connectionSocket, addr=serverSocket.accept()
    print("File Coming...")
    myFile=open("info.txt","wb")
    while True:
        print('receiving data...')
        data = connectionSocket.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        myFile.write(data)
    myFile.close()
    print('Successfully get the file')
    connectionSocket.send("Successfully Transmition")
connectionSocket.close()
