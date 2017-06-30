from socket import *
import _thread
import time

def Get_File(name,fileName):
    global userList
    print('Thread with file name: '+fileName)
    ftpconnectionSocket,addr=ftpServer.accept()
    data = ftpconnectionSocket.recv(1024)
    print(data.decode())
    myFile=open(fileName,"wb+")
    myFile.write(data)
    myFile.close()
    ftpconnectionSocket.close()
    for user in userList:
        user.send(('<a href="'+fileName+'">' +fileName + ' --> Uploaded By --> '+ name + '</a>').encode())
    print('Successfully Getting Information')

def Send_File(fileName):
    ftpconnectionSocket, addr = ftpServer.accept()
    file = open(fileName, 'rb')
    l = file.read()
    file.close()
    ftpconnectionSocket.sendall(l)
    print("Sending File Is Completed!")

def Serve_User(connectionSocket):
    global userList,nameList
    print(len(userList))
    connectionOpen=True
    while connectionOpen:
        sentence = connectionSocket.recv(1024)
        if not sentence:
            print("Connection Is Closed")
        sentence = sentence.decode()
        if sentence == 'j':
            name = connectionSocket.recv(1024)
            nameList.append(name)
            print(len(nameList))
            names=','.join(nameList)
            print(names)
            for user in userList:
                user.sendall(("j").encode('utf-8'))
                time.sleep(.2)
                user.sendall(name)
                time.sleep(.2)
                user.sendall(names)
        if sentence == 'm':
            print("Message Coming...")
            sentence = connectionSocket.recv(1024)
            sentence = sentence.decode()
            print(sentence)
            sentence = "<span>" + name + " -> " + sentence + "</span>"
            sentence = sentence.encode('utf-8')
            for user in userList:
                user.send(sentence)
        elif sentence == 'f':
            print("File Coming...")
            fileName = connectionSocket.recv(1024)
            fileName = fileName.decode()
            print(fileName)
            try:
                _thread.start_new_thread(Get_File, (name,fileName,))
                print("Thread Created")
            except:
                print("Unable To Start New Thread")

        elif sentence=='c':
            print("Going To Remove User From List")
            name = connectionSocket.recv(1024)
            nameList.remove(name)
            userList.remove(connectionSocket)
            connectionSocket.close()
            names = ','.join(nameList)
            for user in userList:
                user.sendall(("c").encode('utf-8'))
                time.sleep(.2)
                user.sendall(name)
                time.sleep(.2)
                user.sendall(names)
            print("Closing Connection...")
            connectionOpen = False

        elif sentence == 'fd':
            print("Going To Send File To A User")
            fileName = connectionSocket.recv(1024)
            fileName = fileName.decode()
            print(fileName)
            try:
                _thread.start_new_thread(Send_File, (fileName,))
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
nameList=[]
while 1:
    connectionSocket, addr = serverSocket.accept()
    userList.append(connectionSocket)
    print ('Connection From Ip:' + str(addr) + ' Is Accepted')
    _thread.start_new_thread(Serve_User, (connectionSocket,))


