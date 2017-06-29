from socket import *
import _thread

def Get_File(name,fileName):
    global userList
    print('Thread with file name:'+fileName)
    ftpconnectionSocket, addr=ftpServer.accept()
    data = ftpconnectionSocket.recv(1024)
    print(data.decode())
    myFile=open(fileName,"wb+")
    myFile.write(data)
    myFile.close()
    ftpconnectionSocket.close()
    for user in userList:
        user.send((fileName + " --> Uploaded By --> "+name).encode())
    print('Successfully Getting Information')

def Serve_User(connectionSocket):
    global userList
    print(len(userList))
    connectionOpen=True
    while connectionOpen:
        sentence = connectionSocket.recv(1024)
        if not sentence:
            print("Connection Is Closed")
        sentence = sentence.decode()
        if sentence == 'j':
            name = connectionSocket.recv(1024)
            welcome=name.decode()+" Joined To Chat"
            welcome=welcome.encode('utf-8')
            for user in userList:
                user.send(welcome)
        if sentence == 'm':
            print("Message Coming...")
            sentence = connectionSocket.recv(1024)
            sentence = sentence.decode()
            print(sentence)
            sentence = name + " -> " + sentence
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
            userList.remove(connectionSocket)
            connectionSocket.close()
            bye = name.decode() + " Left The Chat"
            bye = bye.encode('utf-8')
            for user in userList:
                user.send(bye)
            print("Closing Connection...")
            connectionOpen = False


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
    userList.append(connectionSocket)
    print ('Connection From Ip:' + str(addr) + ' Is Accepted')
    _thread.start_new_thread(Serve_User, (connectionSocket,))


