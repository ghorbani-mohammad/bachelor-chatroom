from socket import *
serverName='m-gh.info'
serverPort=12001
clientSocket=socket(AF_INET,SOCK_STREAM)

fileName=input("Please Insert Name Of Your Text File:")
try:
    myFile=open(fileName+".txt","r")
    num_lines = sum(1 for line in myFile)#Getting Number Of Lines
except:
    print("\n\n\nSomething Goes Wrong. Please Try Again!\n\n")
    exit()
clientSocket.connect((serverName,serverPort))
clientSocket.sendto(bytes([num_lines]),(serverName, serverPort))#Saying Number Of Lines To Server
for line in myFile:
    print(line,end='')
    clientSocket.sendto(line.encode('utf-8'),(serverName, serverPort))
    print(line,end='')
modifiedSentence=clientSocket.recv(1024)
print ('From Server:',modifiedSentence)
clientSocket.close()