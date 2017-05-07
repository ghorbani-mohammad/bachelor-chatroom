from socket import *
serverPort=12001
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
while 1:
    connectionSocket, addr=serverSocket.accept()
    num_lines= connectionSocket.recv(1024)
    num_lines=int.from_bytes(num_lines,byteorder='little')
    myFile=open("file.txt","w")
    for i in range(num_lines):
        print('Waiting To Recieve Line'+ str(i))
        sentence= connectionSocket.recv(1024)
        print(sentence)
        myFile.write(sentence+"\n")
    connectionSocket.send("Successfully Transmition")
    connectionSocket.close()
