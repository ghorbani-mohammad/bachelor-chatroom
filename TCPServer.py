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
    name=name.decode()
    upMsg='<a href="'+fileName+'">' +fileName + ' --> Uploaded By --> '+ name + '</a>'
    upMsg=upMsg.encode('utf-8')
    print(name)
    print(fileName)
    for user in userList:
        user.sendall(("u").encode('utf-8'))
        user.send(upMsg)
    print('Successfully Getting Information')

def Send_File(fileName):
    ftpconnectionSocket, addr = ftpServer.accept()
    file = open(fileName, 'rb')
    l = file.read()
    file.close()
    ftpconnectionSocket.sendall(l)
    print("Sending File Is Completed!")

def Serve_User(connectionSocket):
    print("Join To Serve User")
    global userList,nameList
    print(len(userList))
    name='';
    connectionOpen=True
    while connectionOpen:
        sentence = connectionSocket.recv(1024)
        if not sentence:
            print("Connection Is Closed")
        sentence = sentence.decode()
        if sentence == 'j':
            name = connectionSocket.recv(1024)
            nameList.append(name.decode())
            names = ','.join(nameList)
            print(name.decode())
            print(names)
            names=names.encode('utf-8')
            for user in userList:
                user.sendall(("j").encode('utf-8'))
                user.sendall(names)
        if sentence == 'm':
            print("Message Coming...")
            sentence = connectionSocket.recv(1024)
            sentence = sentence.decode()
            print(sentence)
            sentence = "<span>" + name.decode() + " -> " + sentence + "</span>"
            sentence = sentence.encode('utf-8')
            for user in userList:
                user.sendall(("m").encode('utf-8'))
                user.send(sentence)
        elif sentence == 'u':
            print("File Coming...")
            fileName = connectionSocket.recv(15)
            fileName = fileName.decode()
            print(fileName)
            try:
                _thread.start_new_thread(Get_File, (name,fileName,))
                print("Thread Created")
            except:
                print("Unable To Start New Thread")

        elif sentence=='q':
            print("Going To Remove User From List")
            name = connectionSocket.recv(10)
            name=name.decode()
            i=nameList.index(name)
            nameList[0],nameList[i]=nameList[i],nameList[0]
            names = ','.join(nameList)
            userList.remove(connectionSocket)
            nameList.remove(name)
            connectionSocket.close()
            names=names.encode('utf-8')
            for user in userList:
                user.sendall(("q").encode('utf-8'))
                user.sendall(names)
            print("Closing Connection...")
            connectionOpen = False

        elif sentence == 'd':
            print("Going To Send File To A User")
            fileName = connectionSocket.recv(15)
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


