from socket import *
import _thread

def Get_File(fileName):
    print('Thread with file name:'+fileName)
    ftpconnectionSocket, addr=ftpServer.accept()
    data = ftpconnectionSocket.recv(1024)
    print(data.decode())
    myFile=open(fileName,"wb+")
    myFile.write(data)
    myFile.close()
    ftpconnectionSocket.send((fileName+" Uploaded By ").encode())
    ftpconnectionSocket.close()
    print('Successfully Getting Information')

def Serve_User(connectionSocket):
    global userList
    print(len(userList))
    while 1:
        sentence = connectionSocket.recv(1024)
        if not sentence:
            break
        sentence = sentence.decode()
        if sentence == 'm':
            print("Message Coming...")
            sentence = connectionSocket.recv(1024)
            sentence = sentence.decode()
            print(sentence)
            capitalizedSentence = sentence.upper()
            capitalizedSentence = capitalizedSentence.encode('utf-8')
            connectionSocket.send(capitalizedSentence)
        elif sentence == 'f':
            print("File Coming...")
            fileName = connectionSocket.recv(1024)
            fileName = fileName.decode()
            print(fileName)
            try:
                _thread.start_new_thread(Get_File, (fileName,))
                print("Thread Created")
            except:
                print("Unable To Start New Thread")
serverPort=12000
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

ftpServerPort=12001
ftpServer=socket(AF_INET,SOCK_STREAM)
ftpServer.bind(('',ftpServerPort))
ftpServer.listen(1)

print ('The server is ready to receive')

userList=[]
while 1:
    connectionSocket, addr = serverSocket.accept()
    userList.appendd(connectionSocket)
    print ('Connection From Ip:' + str(addr) + ' Is Accepted')
    _thread.start_new_thread(Serve_User, (connectionSocket,))


