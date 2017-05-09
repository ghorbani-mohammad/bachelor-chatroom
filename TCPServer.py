from socket import *
serverPort=12000
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
print ('The server is ready to receive')
serverSocket.listen(10)
connectionSocket, addr=serverSocket.accept()
print ('Connection From Ip:'+str(addr)+' Is Accepted')
while 1:
    sentence= connectionSocket.recv(1024)
    if not sentence:
        break
    sentence=sentence.decode()
    if sentence=='m':
        print("Message Coming...")
        sentence= connectionSocket.recv(1024)
        sentence=sentence.decode()
        print(sentence)
        capitalizedSentence=sentence.upper()
        capitalizedSentence=capitalizedSentence.encode('utf-8')
        connectionSocket.send(capitalizedSentence)
    elif sentence=='f':
        try:
            print("File Coming...")
            fileName=connectionSocket.recv(1024)
            fileName=fileName.decode()
            print(fileName+"\n")
            numLines=connectionSocket.recv(1024)
            numLines=int.from_bytes(numLines,byteorder='little')
            print("\n"+numLines)
            myFile=open("info.txt","w")
            print("Create File")
        except:
            connectionSocket.close()
connectionSocket.close()
